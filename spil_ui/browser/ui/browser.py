# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2021 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""

import os
import sys
import logging
from collections import OrderedDict

# Uses Qt.py
from Qt import QtCore, QtCompat, QtWidgets
from spil.util.log import DEBUG, setLevel, WARN

from spil.util.utils import uniqfy  # FIXME: deep import

from spil_ui.browser.ui.qt_helper import addListWidgetItem, clear_layout, addTableWidgetItem, table_css

# FS and Files must be abstracted / to a data delegate
from spil import FS, Sid, SpilException, conf
from data.files import Files
import engines
from spil_ui.util.dialogs import Dialogs

log = logging.getLogger('browser')

UserRole = QtCore.Qt.UserRole
ui_path = os.path.join(os.path.dirname(__file__), 'qt/browser.ui')

searchers = ['*', ',', '>', '<']
entity_version_slit = 'version'  # key that separates entity blocs/lists representation and the table bloc representation
table_bloc_columns = ['Sid', 'Time', 'Size']
table_bloc_callbacks = ['getTime', 'getSize']  #SMELL a bit.

class Browser(QtWidgets.QMainWindow):

    cb = QtWidgets.QApplication.clipboard()  # TODO: use

    def __init__(self, search=None):
        super(Browser, self).__init__()
        QtCompat.loadUi(ui_path, self)

        # init sources
        self.data = Files()  # TODO: data framework
        self.uio = Dialogs()
        self.engine = engines.get()
        self.sid_history = conf.sid_usage_history
        print('Loaded engine {}'.format(self.engine))

        self.buttons = []
        self.previous_sid = Sid()
        self.previous_search = Sid()

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
        print(search)

        self.current_sid = Sid()  # TODO: if search returns a single Sid, make it the current. (or the first from search?)

        self.connect_events()

        self.launch_search(search)
        # self.boot_entities()
        # self.init_actions()

    # Build / Edit UI
    def boot_entities(self):
        """ Builds root part: project, type """
        clear_layout(self.entities_lo)
        self.sid_widgets = OrderedDict()
        self.versions_tw.clear()
        self.build_entities()

    def build_entities(self):

        for key in self.search.data.keys():  # traverses search_sid by key: project, type, ...

            if key == 'version':
                self.build_versions()
                return

            if self.sid_widgets.get(key):  # if the widget already exists, we get it...
                list_widget = self.sid_widgets.get(key)
                if self.search.get(key) in searchers or not self.current_sid.get(key):  # need to clear entities below
                    list_widget.clear()
                    self.clear_entities()
            else:
                list_widget = self.create_entity_widget(key)  # ...else we create it

            if list_widget.count():
                continue

            found = FS().get(self.search.get_as(key).get_with(key=key, value='*'), as_sid=False)

            for i in sorted(list(found)):
                i = Sid(i)
                item = addListWidgetItem(list_widget, i.get_as(key), i.get(key))

                if i.get_as(key) == self.search.get_as(key):
                    item.setSelected(True)
                    list_widget.setCurrentItem(item)
                    self.current_sid = i.get_as(key)
                    self.update_current()

            list_widget.itemClicked.connect(self.select_search)

            if self.search.get(key) in searchers:
                break

        """  #TODO: tab order
        for i in range(len(self.sid_widgets))-1:
            item.setTabOrder(self.textboxA, self.textboxB)
            self.entities_lo.setTabOrder(self.sid_widgets)
        """

    def build_versions(self):  #IDEA: load only last versions, with a drop down for all versions (https://openpype.io/docs/artist_tools#load-another-version)

        parent = self.versions_tw
        parent.clear()

        parent.setColumnCount(len(table_bloc_columns))
        parent.setHorizontalHeaderLabels(table_bloc_columns)

        parent.verticalHeader().setVisible(False)
        parent.verticalHeader().setDefaultSectionSize( 30 )

        if self.search:

            if self.search.get('ext'):
                search = self.search.get_with(version='*', state='*')
                search = search.string
            else:
                search = self.search.get_with(version='*', state='*', ext='maya,movie')  # FIXME
                # self.search = self.search.get_with(version='*', state='*', ext='*')  # FIXME
                search = search.string

            #if self.search.get_as('version'):
            #    search = self.search.get_as('version').string + '/**'  # FIXME : this is not nice.

            print('now searching')
            print(search)
            children = sorted(list(FS().get(search, as_sid=False)))

            parent.setRowCount(len(children))
            for row, sid in enumerate(children):
                sid= Sid(sid)
                item = addTableWidgetItem(parent, sid, sid, row=row, column=0)

                for i, func in enumerate(table_bloc_callbacks):
                    func = getattr(self.data, func)
                    addTableWidgetItem(parent, None, func(sid), row=row, column=i+1)

                print('{} // {} ?'.format(sid, self.search))
                if sid == self.search:  # FIXME: must also work during update
                    item.setSelected(True)
                    parent.setCurrentItem(item)
                    self.current_sid = sid
                    self.update_current()

                parent.itemClicked.connect(self.select_search)

            parent.setStyleSheet(table_css)
            parent.resizeColumnsToContents()
            if parent.columnWidth(0) < 120:  #TODO Make dynamic
                parent.setColumnWidth(0, 260)
                parent.setColumnWidth(1, 140)
                parent.setColumnWidth(2, 100)

    def clear_entities(self):
        """
        Clears entity widgets that are not in the search Sid (below the search).
        If needed calls clear_versions. (#TODO makethis code better readable)
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

    # Update / SID IO
    """
    The circle is basically:
    search -> results -> selection / input -> current -> search
    
    In detail the circle is:
    - start with a search sid
    - potentially add search terms to search sid, typically : /* at the end.
    - boot / fill entities and versions with search sid and search results
    - select with values from search sid by default -> we have a current sid 
    - wait for user input -> we update the current sid
    - on signal, we update the search sid, current -> search, and loop again.
    """
    def select_search(self, item = None, sid = None):
        print('In select search, from {} -> {}'.format(self.sender().objectName(), item.data(UserRole)))
        sid = item.data(UserRole)
        self.launch_search(sid)

    def input_search(self):
        self.launch_search(self.input_sid_le.text())

    def edit_search(self, search_sid):
        """
        If the search has no searchers ("*", ",", ...) it needs edit.
        """
        if any((True if s in str(search_sid) else False for s in searchers)):  # we check this first, because the Sid might not be "defined", eg. FTOT/A/PRP/VIAL/RIG/**/mov
            print('edit_search {} -> {}'.format(search_sid, searchers))
            return search_sid

        if search_sid.is_leaf():
            return search_sid

        return Sid(str(search_sid) + '/*')

    def launch_search(self, search_sid):
        """
        Receives an updated search, to start a new search cycle.
        Called from history or the search sid input field.
        """
        print('New search cycle: ' + str(search_sid))
        search_sid = Sid(search_sid)

        # check if the search needs update
        search_sid = self.edit_search(search_sid)
        self.search = search_sid
        self.input_sid_le.setText(self.search.string)

        # launch new cycle
        print('New search cycle launch: ' + str(search_sid))
        if (search_sid.basetype == search_sid.type) or not self.previous_search:  # a way to say its a root type #FIXME
            self.boot_entities()
        else:
            self.build_entities()  # or rebuild root or versions ...

        # self.previous_search = self.search

    def update_current(self):  #FIXME: rename
        self.current_sid_lb.setText(self.current_sid.string)
        # self.input_sid_le.setText(self.search.string)
        if self.current_sid != self.previous_sid:
            self.previous_sid = self.current_sid
            self.init_actions()

    """
    def refresh_sid(self):  #TODO: here also select the columns according to Sid. Must be a perfect circle.
        pass
    
    def get_current_sid(self, item=None, sid=None):

        if item:
            print(item)
            sid = item.data(UserRole)

        if sid:
            print(sid)
            self.current_sid = sid
            self.current_to_search()
            self.update_current()

            if sid.basetype == sid.type:  # a way to say its a root type #FIXME
                self.boot_entities()
            else:
                self.build_entities()  # or rebuild root or versions ...
    
    def current_to_search(self):
        '''
        Updates the search Sid depending on the Current Sid
        Cases:
        - we just add a '*' at the end
        - we keep the search, but update keys existing in current sid
        - need to handle entities and version searches
        - how handle non Sid Searches ?
        '''
        search = self.search.copy()

        for key in search.data.keys():
            if self.current_sid.get(key):
                self.search = self.search.get_with(key=key, value=self.current_sid.get(key))
        else:
            self.search = Sid(self.current_sid)
        # if "incomplete", add a star at the end
        if not self.current_sid.is_leaf():
            self.search = Sid(str(self.search) + '/*')
    """

    def set_sid_from_history(self):
        selected = self.sid_history_cb.itemText(self.sid_history_cb.currentIndex())
        if selected:
            print('selected ' + selected)
            self.launch_search(Sid(selected))

    # Actions
    def init_actions(self):

        self.actions_gb.setTitle(self.engine.name.replace('_', ' ').capitalize())
        for b in self.buttons:
            b.setVisible(False)
            b.deleteLater()
        self.buttons = []

        for feature in self.engine.get_actions(self.current_sid):
            button = QtWidgets.QPushButton(feature.replace('_', ' ').capitalize(), self)
            # button.setToolTip((getattr(self.engine, feature).__doc__ or '').strip().replace('\t', ''))
            button.setObjectName(feature)
            button.clicked.connect(self.run_actions)
            self.actions_hl.addWidget(button)
            self.buttons.append(button)

    def run_actions(self):  # TODO: more advanced features with parameters or options

        if not self.current_sid:
            return

        sid = self.current_sid

        sender = self.sender().objectName()

        log.debug('sender: ["{0}"]'.format(sender))

        if sender == 'versions_tw':  # double click
            sender = self.engine.implements[0] if self.engine.implements else 'explore'

        if sender in self.engine.needs_confirm:
            if not self.uio.warn('This function may alter the scene and is not undoable. Are you sure?', withCancel=True):
                return

        func = getattr(self.engine, sender)

        if not func:
            log.warn('Function "{0}" does not exist'.format(func))
            return

        log.debug('Calling "{0}" with "{1}" '.format(func, sid))
        try:

            func(sid)  # TODO : options, return value for user feedback
            self.fill_history(sid)  # done at the end because sid might have changed

        except RuntimeError as e:
            self.uio.error('Could not call "{0}" with "{1}".\nError : {2}'.format(func, sid, e))

        except SpilException as e:
            self.uio.error('{0}'.format(e))

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
        self.versions_tw.doubleClicked.connect(self.run_actions)
        self.sid_history_cb.currentIndexChanged.connect(self.set_sid_from_history)

    def showEvent(self, arg=None):
        self.sid_history = conf.sid_usage_history  # TODO : test this : no real refresh
        self.fill_history()

    def closeEvent(self, arg=None):
        try:
            conf.set('sid_usage_history', self.sid_history)
        except:
            pass

if __name__ == '__main__':

    setLevel(WARN)

    app = QtWidgets.QApplication(sys.argv)

    sid = 'FTOT/A/CHR/COCO/MOD/V002/WIP/mov'
    sid = 'FTOT/S/SQ0001/SH0020/LAY/V002/WIP/mov'
    sid = 'FTOT/S/SQ0001/SH0020/LAY/V002/WIP/ma'
    # 'FTOT/S/SQ0001/SH0020/LAY/*/*/movie,maya'
    # sid = '' # IMPORTANT: TEST THIS ALSO
    # sid = 'raj/a/char/romeo'
    sid = Sid(sid)
    print(sid)
    search = sid.get_with(version='*', state='*', ext='maya,movie')
    print('search:')
    print(search)
    for i in FS().get(search):
        print(i)


    win = Browser(search=sid)
    win.show()

    app.exec_()

