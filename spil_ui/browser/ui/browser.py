# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2022 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""

"""
TODO:
- tab order (and arrows left/right) for mouseless navigation
- arrow keys (up/down) in listwidgets
- last action in conf for double click / default action
- actions refresh browser when done

    The Search circle is basically:
    search -> results -> selection / input -> current -> search
    
    In detail the circle is:
    - start with a search sid
    - potentially add search terms to search sid, typically : /* at the end.
    - boot / fill entities and versions with search sid and search results
    - select with values from search sid by default -> we have a current sid 
    - wait for user input -> we update the current sid
    - on signal, we update the search sid, current -> search, and loop again.
    
"""
import os
from spil import logging
from collections import OrderedDict

# Uses Qt.py
from Qt import QtCore, QtCompat, QtWidgets, QtGui
# from Qt.QtWidgets import QMenu, QAction
# from Qt.QtCore import Qt

from spil.util.utils import uniqfy  # FIXME: deep import

from spil_ui.browser.ui.qt_helper import addListWidgetItem, clear_layout, addTableWidgetItem, table_css

# FS and Files are abstracted / to a data delegate
from spil import Data as FS, Sid, SpilException, conf
from pipe_action import engines  #FIXME: remove this
from spil_ui.browser.ui.action_handler import get_action_handler

import spil.util.log as sl
sl.setLevel(sl.ERROR)

log = logging.get_logger(name="spil_ui")
log.setLevel(logging.INFO)

UserRole = QtCore.Qt.UserRole
ui_path = os.path.join(os.path.dirname(__file__), 'qt/browser.ui')

from spil_ui.conf import searchers, is_leaf
from spil_ui.conf import table_bloc_columns, table_bloc_attributes, extension_filters
from spil_ui.conf import search_reset_keys, basetype_to_cut, basetype_to_leafkey, basetype_clipped_versions

""" WIP for dynamic options
version_filters = {
                    'shot': {'state': ['WIP', 'OK']},
                    'render': {'state': ['WIP', 'OK']},
                  }

basetype_to_extensions = {
                        'shot': ['maya', 'movie', 'cache'],
                        'render': ['img'],
                         }
"""

sid_colors = {'published': QtGui.QColor(207, 229, 85)}

#Right clic : Open unloaded, Copy Sid, Add to history, Open OK, edit comment, edit json
#TODO: perfect Sid paste, including abc (and add to history ?), tab order, arrow keys
class Browser(QtWidgets.QMainWindow):

    cb = QtWidgets.QApplication.clipboard()  # TODO: use

    def __init__(self, search=None):
        super(Browser, self).__init__()
        QtCompat.loadUi(ui_path, self)
        self.setWindowTitle('{} - Browser'.format('Pikko @ Kombbo'))

        # init sources
        self.engine = engines.get()
        self.action_handler = get_action_handler()
        self.action_handler.init(self, self.central_layout, callback=self.fill_history)
        log.debug('Loaded action handler {}'.format(self.action_handler))
        self.sid_history = conf.sid_usage_history
        log.debug('Loaded engine {}'.format(self.engine))

        self.buttons = []
        self.boxes = []
        self.search = None
        self.previous_sid = Sid()

        # Init of the SearchSid
        # Either passed argument, or current from engine, or last from history, or empty Sid
        if search:
            search = Sid(search)
        elif self.engine.get_current_sid():
            search = self.engine.get_current_sid()
        elif self.sid_history:
            search = Sid(self.sid_history[-1])
        else:
            search = Sid('*')
        log.debug(search)

        self.ok_cb.setVisible(False)  #FIXME: temp
        self.wip_cb.setVisible(False)
        self.state_gb.setVisible(False)
        self.init_extension_filters()

        self.current_sid = Sid()
        self.connect_events()
        self.launch_search(search)

    # Build / Edit UI
    def boot_entities(self):
        """ Builds root part: project, type """
        clear_layout(self.entities_lo)
        self.sid_widgets = OrderedDict()
        self.versions_tw.clear()
        self.build_entities()

    def build_entities(self):

        if '/**' in self.search.string:
            search = Sid(self.search.string.split('/**')[0])
        else:
            search = self.search.copy()

        for key in search.data.keys():  # traverses search_sid by key: project, type, ...

            if self.sid_widgets.get(key):  # if the widget already exists, we get it...
                list_widget = self.sid_widgets.get(key)
                if search.get(key) in searchers or not self.current_sid.get(key):  # need to clear entities below
                    list_widget.clear()
                    self.clear_entities()
            else:
                list_widget = self.create_entity_widget(key)  # ...else we create it

            if list_widget.count():
                continue

            found = FS().get(search.get_as(key).get_with(key=key, value='*'), as_sid=False)

            for i in sorted(list(found)):
                i = Sid(i)
                if not i.get_as(key):  # erroneous Sid  TODO: move this double check as option in the search
                    # print('erronoues {}'.format(i))
                    continue
                item = addListWidgetItem(list_widget, i.get_as(key), i.get(key))

                if i.get_as(key) == search.get_as(key):
                    item.setSelected(True)
                    list_widget.setCurrentItem(item)
                    self.current_sid = i.get_as(key)
                    self.update_current_sid()

            # list_widget.itemDoubleClicked.connect(self.select_search)
            list_widget.itemClicked.connect(self.select_search)
            # list_widget.itemSelectionChanged.connect(self.select_search)

            #list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
            #list_widget.customContextMenuRequested.connect(self.openMenu)

            list_widget.setFixedWidth(list_widget.sizeHintForColumn(0) + 2 * list_widget.frameWidth() + 20)

            if search.get(key) in searchers:
                break

            if key == basetype_to_cut.get(search.basetype, 'task'):  # 'shot':  # 'task':
                self.build_versions()
                return

        log.debug('Done build_entities. - ' + self.search.string)

        if '/**' in self.search.string:
            self.build_versions()

        """  #TODO: tab order
        for i in range(len(self.sid_widgets))-1:
            item.setTabOrder(self.textboxA, self.textboxB)
            self.entities_lo.setTabOrder(self.sid_widgets)
        """

    def build_versions(self):  # IDEA: load only last versions, with a drop down for all versions (https://openpype.io/docs/artist_tools#load-another-version)

        parent = self.versions_tw
        parent.clear()

        parent.setColumnCount(len(table_bloc_columns))
        parent.setHorizontalHeaderLabels(table_bloc_columns)

        parent.verticalHeader().setVisible(False)
        parent.verticalHeader().setDefaultSectionSize(30)

        log.debug('build_versions start: ' + self.search.string)

        log.debug('search on start {}'.format(self.search))

        if self.search:  # if the current search is defined, typed. #FIXME: not clear. #SMELL

            if '/**' in self.search.string:
                search = self.search.string
            else:
                # we keep the global self.search but change fields for version, state, ext.
                key = basetype_to_cut.get(self.search.basetype, 'task')
                if self.search.get_as(key):
                    search = self.search.get_as(key).string + '/**'
                else:
                    search = None

        else:

            search = self.search.string

        # print(f'intermediate: search)

        if search:

            ext_filter = []
            for box in self.boxes:
                box_text = box.text()
                if box.isChecked():
                    ext_filter.append(box_text)

            if '/**' in search and ext_filter:
                if search.count('?'):  # sid contains URI ending. We put it aside, and later append it back
                    search, uri = search.split('?', 1)
                else:
                    uri = ''
                search = search.split('/**')[0] + '/**/' + ','.join(ext_filter) + ('?' + uri if uri else '')

            self.input_sid_le.setText(search)

            search = search + ('?version=>' if self.last_cb.isChecked() else '')
            search = search + '?state=~WIP'  # FIXME: temporary hide OK
            if self.search.basetype in basetype_clipped_versions and not ext_filter:
                search = search.replace('**', '*')

            log.debug('Final search: {}'.format(search))

            # dirty technique to force single frame search for speed.
            # children = sorted(list(FS().get(search + '?state=WIP' + ('&frame=0101' if self.search.basetype == 'render' else ''), as_sid=False)))
            children = sorted(list(FS().get(search, as_sid=False)))

            children = list(filter(bool, [Sid(s) for s in children]))

            # above is same as:
            # children = sorted(list(FS().get(search, as_sid=True)))
            # which is potentially slower in PY2. TODO: profile
            # we need to limit to valid Sids to avoid pseudo Sids to be listed (CHR_CRASH_SUB_WIP_ "V001_autosave_1" version
            # dont forget to comment sid = Sid(sid) line 270

            parent.setRowCount(len(children))
            for row, sid in enumerate(children):
                # sid = Sid(sid)
                sid_color = sid_colors.get('published') if sid.get_with(state='OK').exists() else None
                item = addTableWidgetItem(parent, sid, sid, row=row, column=0, fgcolor=sid_color)

                for i, attr in enumerate(table_bloc_attributes):
                    addTableWidgetItem(parent, sid, sid.get_attr(attr) or '', row=row, column=i+1)

                # log.debug('{} // {} ?'.format(sid, self.search))
                if sid == self.search:  # FIXME: must also work during update
                    item.setSelected(True)
                    parent.setCurrentItem(item)
                    self.current_sid = sid
                    self.update_current_sid()

                # parent.itemClicked.connect(self.select_search)

            parent.setStyleSheet(table_css)
            parent.resizeColumnsToContents()
            if parent.columnWidth(0) < 120:
                parent.setColumnWidth(0, 260)
                parent.setColumnWidth(1, 140)
                parent.setColumnWidth(2, 100)

    def clear_entities(self):
        """
        Clears entity widgets that are not in the search Sid (below the search).
        If needed calls clear_versions. (#TODO make this code better readable)
        """

        skip = True
        for key in self.sid_widgets.keys():
            if not self.search.get(key):  # or not self.current.get(key):
                skip = False
            if skip:
                continue
            list_widget = self.sid_widgets.get(key)
            list_widget.clear()
        # if not skip:
        self.clear_versions()

    def clear_versions(self):
        self.versions_tw.clear()

    def set_sid_from_history(self):  # TODO: history handler
        selected = self.sid_history_cb.itemText(self.sid_history_cb.currentIndex())
        if selected:
            log.debug('selected ' + selected)
            self.launch_search(Sid(selected))

    def select_search(self, item=None):
        """
        Called by click on an entity widget (project, type, asset/shot, etc.) or the version table.
        Receives the clicked sid.

        Launches the new search, either "sticky" or "reset".
        Sticky: the self.search is kept, only updated with the clicked sids keytype (last key)
        Reset: the clicked sid replaces the self.search all over.

        If the click comes from the version table, it is "reset".
        Sticky search is possible only if the self.search is typed.
        If the clicked sids keytype is of certain type, as defined in "search_reset_keys" we use "reset".
        """
        sid = item.data(UserRole)
        log.debug('Select search: item sid="{}", self.search="{}"'.format(sid, self.search))

        if self.sender() == self.versions_tw:
            self.launch_search(sid)
        else:
            sid = Sid(sid)
            key = sid.keytype
            if self.search.type and key not in search_reset_keys:
                # TODO: implement this in the Sid, and document
                search = Sid(str(self.search) + '?{}=~{}'.format(key, sid.get(key)) )  # .get_with(key=key, value='~' + sid.get(key))  {
                self.launch_search(search)
            else:
                self.launch_search(sid)

    def input_search(self):
        """
        Called when the input sid lineEdit "input_sid_le" is triggered.
        Launches a new search.
        """
        log.debug('input_search {}'.format(self.input_sid_le.text()))
        self.launch_search(self.input_sid_le.text())

    def edit_search(self, search_sid):  # TODO: factorize and simplify xxx_search methods
        """
        If the search has no searchers ("*", ",", ...) it needs edit.
        """
        if any(s in str(search_sid) for s in searchers):  # we check this first, because the Sid might not be "defined", eg. FTOT/A/PRP/VIAL/RIG/**/mov
            log.debug('edit_search {} -> {}'.format(search_sid, searchers))
            return search_sid

        if is_leaf(search_sid):
            return search_sid

        return Sid(str(search_sid) + '/*')

    def launch_search(self, search_sid):
        """
        Main entry point for a new search.
        Called either by:
        - __init__ (browser start),
        - set_sid_from_history (sid history menu),
        - input_search (search sid line edit), or
        - select_search (click select a sid)

        Launches a new search cycle.
        - instanciates the Sid
        - calls edit_search: add search criterias ('*') if needed.
        - sets self.search
        - sets the input field
        - calls boot_entities: triggers UI update with the new columns, table, buttons
        """
        log.debug('New search cycle: ' + str(search_sid))
        search_sid = Sid(search_sid)

        # if it is a leaf (typically a file), we keep the current search as long as it matches
        if is_leaf(search_sid) and search_sid.match(self.search):
            log.debug('We selected File Sid "{}" - Setting Current Sid but keeping search sid '.format(search_sid))
            self.current_sid = search_sid
            self.update_current_sid()
            return

        # check if the search needs update
        search_sid = self.edit_search(search_sid)
        self.search = search_sid
        self.input_sid_le.setText(self.search.string)

        self.boot_entities()

    def update_current_sid(self):
        self.current_sid_lb.setText(self.current_sid.string)
        if self.current_sid != self.previous_sid:
            self.previous_sid = self.current_sid
            self.action_handler.update(self.current_sid)

    def init_extension_filters(self):
        """
        Creates check boxes for extensions, from given config.
        """

        filters = extension_filters

        if not filters:
            return

        groupBox = QtWidgets.QGroupBox("Extensions", self)
        vbox = QtWidgets.QVBoxLayout(self)

        for ext in filters:
            box = QtWidgets.QCheckBox(ext, self)
            box.setObjectName('ext_' + ext)
            box.clicked.connect(self.build_versions)
            vbox.addWidget(box)
            self.boxes.append(box)

        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        self.engine_la.addWidget(groupBox)

    # Utils
    def create_entity_widget(self, key):

        list_widget = QtWidgets.QListWidget()
        list_widget.setObjectName(key)
        self.entities_lo.addWidget(list_widget)
        self.sid_widgets[key] = list_widget
        return list_widget

    def fill_history(self, sid=None):

        self.sid_history_cb.clear()

        if sid:
            self.sid_history.append(str(sid))
            self.sid_history = uniqfy(self.sid_history, reverse=True)
            if len(self.sid_history) > conf.sid_usage_history_len:
                self.sid_history.pop(0)

            self.sid_history_cb.addItem(str(sid))
        else:
            self.sid_history_cb.addItem('')

        for sid in reversed(self.sid_history):
            """ #TODO: limit history to current engine
            if not self.history_all_CB.isChecked():
                tmp = Sid(sid=str(sid))
                if tmp.get('ext') and tmp.get('ext') != conf.context_to_ext.get(self.ui_context):
                    continue
            """
            self.sid_history_cb.addItem(str(sid))

    def connect_events(self):
        self.input_sid_le.returnPressed.connect(self.input_search)
        self.sid_history_cb.currentIndexChanged.connect(self.set_sid_from_history)
        self.versions_tw.itemClicked.connect(self.select_search)
        self.last_cb.clicked.connect(self.build_versions)
        # QtWidgets.QShortcut(QtCore.Qt.Key_Up, self.centralwidget, self.select_search)  # TODO: arrow keys in listwidgets

    def showEvent(self, arg=None):
        self.sid_history = conf.sid_usage_history  # TODO : test this : no real refresh
        self.fill_history()

    def closeEvent(self, arg=None):
        try:
            conf.set('sid_usage_history', self.sid_history)
        except Exception:
            pass


def open_browser(sid=None, do_new=False):

    global browser_window
    try:
        if not browser_window:
            browser_window = None
    except:
        browser_window = None

    if do_new or not browser_window:
        browser_window = Browser(search=sid)
        browser_window.show()
    else:
        browser_window.activateWindow()
        browser_window.raise_()
        browser_window.setWindowState(browser_window.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        browser_window.show()

    return browser_window


def app(sid=None):

    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    open_browser(sid)
    app.exec_()


if __name__ == '__main__':

    # import cProfile  # profiling
    from spil.util.log import DEBUG, setLevel, WARN, ERROR, INFO
    setLevel(ERROR)

    sid = ''  # FTOT/S/SQ0001/SH0020/LAY/V002/WIP/ma'

    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    open_browser(sid)
    # cProfile.run('open_browser("FTOT/S/SQ0001/SH0020/LAY/V002/WIP/ma", do_new=True)', sort=1)
    # open_browser(sid)
    app.exec_()
