"""
This file is part of spil_ui, a UI using SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2024 Michael Haussmann, spil@xeo.info

SPIL_UI is free software and is distributed under the MIT License. See LICENSE file.
"""
from __future__ import annotations
from typing import Optional

"""
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

# Uses qtpy
import qtpy
from qtpy import QtCore, QtWidgets, QtGui

from spil.util.utils import uniqfy  # TODO: refactor sid history
from spil_ui.browser.ui.qt_helper import (
    addListWidgetItem,
    clear_layout,
    addTableWidgetItem,
    table_css,
)
from spil import FindInAll as Finder, Sid, conf

import spil.util.log as sl

sl.setLevel(sl.ERROR)

log = logging.get_logger(name="spil_ui")
log.setLevel(logging.INFO)

UserRole = QtCore.Qt.UserRole
ui_path = os.path.join(os.path.dirname(__file__), "qt/browser.ui")

from spil_ui.conf import is_leaf, browser_title, get_action_handler
from spil_ui.conf import table_bloc_columns, table_bloc_functions, extension_filters
from spil_ui.conf import search_reset_keys, basetype_to_cut, basetype_clipped_versions

sid_colors = {"published": QtGui.QColor(85, 230, 85)}


class Browser(QtWidgets.QMainWindow):
    """
    The Browser window launches searches for the current search sid.
    The resulting "current Sid" is represented in clickable parts:
    - on the lefts the "entity" columns, on for each part
    - on the right the "version" table, one line for earch Sid

    A new search is launched when either
    - a column selection changes
    - the "search Sid" field is edited
    - the sid history (last used Sids) is changed

    An ActionHandler uses the selected Sid to handle actions.
    Typically showing Buttons and running functions.
    """

    # cb = QtWidgets.QApplication.clipboard()  # TODO: use

    def __init__(self, search=None):
        super(Browser, self).__init__()
        # For some ominous reason, this does not work:
        # qtpy.uic.loadUi(ui_path, self)
        from qtpy.uic import loadUi
        loadUi(ui_path, self)
        self.setWindowTitle(f"{browser_title} - Browser")

        # init sources
        self.action_handler = get_action_handler()
        self.action_handler.init(self, self.central_layout, callback=self.fill_history)
        log.debug(f"Loaded action handler {self.action_handler}")
        self.sid_history = conf.sid_usage_history

        self.buttons = []
        self.boxes = []
        self.search = None
        self.previous_sid = Sid()

        # Init of the SearchSid: either argument, or last from history, or empty Sid
        if search:
            search = Sid(search)
        elif self.sid_history:
            search = Sid(self.sid_history[-1])
        else:
            search = Sid("*")
        log.debug(search)

        # State filter  work / publish # FIXME: hard coded, to be changed
        # self.state_gb.setVisible(False)
        # self.publish_cb.setVisible(False)
        # self.work_cb.setVisible(False)
        self.publish_cb.setText('publish')
        self.work_cb.setText('work')

        self.init_extension_filters()

        self.current_sid = Sid()
        self.connect_events()
        self.launch_search(search)

    # Build / Edit UI
    def boot_entities(self):
        """Builds root part: project, type"""
        clear_layout(self.entities_lo)
        self.sid_widgets = OrderedDict()
        self.versions_tw.clear()
        self.build_entities()

    def build_entities(self):
        """
        Builds "Entity" (Asset or Shot) columns.

        The columns are list_widgets.
        They are build in a loop, according to the parts of the search_sid.

        This method is followed by "build_versions".
        Build_entities stops either:
        - when there are no parts left (eg "hamlet/s/sq010" has 3 parts)
        - when it hits a "cut" key (as configured in "basetype_to_cut")

        It then goes to "build_versions"
        - if "/**" is in the search
        """

        if "/**" in self.search.string:
            search = Sid(self.search.string.split("/**")[0])
        else:
            search = self.search.copy()

        # traverses search_sid by key: project, type, ...
        for key in search.fields.keys():

            # if the widget already exists, we get it...
            if self.sid_widgets.get(key):
                list_widget = self.sid_widgets.get(key)

                # need to clear entities below
                if search.get(key) in conf.search_symbols or not self.current_sid.get(
                    key
                ):
                    list_widget.clear()
                    self.clear_entities()
            else:
                list_widget = self.create_entity_widget(key)  # ...else we create it

            if list_widget.count():
                continue

            found = Finder().find(
                search.get_as(key).get_with(key=key, value="*"), as_sid=False
            )

            for i in sorted(list(found)):
                i = Sid(i)
                # TODO: move this double check as option in the search
                if not i.get_as(key):  # erroneous Sid
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
            # list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
            # list_widget.customContextMenuRequested.connect(self.openMenu)

            list_widget.setFixedWidth(
                list_widget.sizeHintForColumn(0) + 2 * list_widget.frameWidth() + 20
            )

            if search.get(key) in conf.search_symbols:
                break

            if key == basetype_to_cut.get(search.basetype, "task"):
                self.build_versions()
                return

        log.debug(f"Done build_entities. - {self.search.string}")

        if "/**" in self.search.string:
            self.build_versions()

        """  #TODO: tab order
        for i in range(len(self.sid_widgets))-1:
            item.setTabOrder(self.textboxA, self.textboxB)
            self.entities_lo.setTabOrder(self.sid_widgets)
        """

    # IDEA: load only last versions, with a drop-down for all versions
    def build_versions(self):
        """
        Builds a table widget for the last part of the Sid.
        This method is launched after "build_entities" has finished.

        The current search sid is modified to add extension and "last", as given by the checkboxes.
        """

        parent = self.versions_tw
        parent.clear()

        parent.setColumnCount(len(table_bloc_columns))
        parent.setHorizontalHeaderLabels(table_bloc_columns)

        parent.verticalHeader().setVisible(False)
        parent.verticalHeader().setDefaultSectionSize(30)

        log.debug("build_versions start: " + self.search.string)

        log.debug("search on start {}".format(self.search))

        if self.search:  # Untyped evaluates to False.

            if "/**" in self.search.string:
                search = self.search.string
            else:
                # we keep the global self.search but change fields for version, state, ext.
                key = basetype_to_cut.get(self.search.basetype, "task")
                if self.search.get_as(key):
                    search = self.search.get_as(key).string + "/**"
                else:
                    search = None

        else:

            search = self.search.string

        if search:

            ext_filter = []
            for box in self.boxes:
                box_text = box.text()
                if box.isChecked():
                    ext_filter.append(box_text)

            if "/**" in search and ext_filter:

                # sid contains query ending. We put it aside, and later append it back
                if search.count("?"):
                    search, query = search.split("?", 1)
                else:
                    query = ""

                search = (
                    search.split("/**")[0]
                    + "/**/"
                    + ",".join(ext_filter)
                    + ("?" + query if query else "")
                )

            self.input_sid_le.setText(search)

            # FIXME: hard coded -> config
            search = search + ("?version=>" if self.last_cb.isChecked() else "")
            if self.work_cb.isChecked() and self.publish_cb.isChecked():
                search = search + ('?state=~w,p')
            else:
                search = search + ('?state=~w' if self.work_cb.isChecked() else "")
                search = search + ('?state=~p' if self.publish_cb.isChecked() else "")
            if self.search.basetype in basetype_clipped_versions and not ext_filter:
                search = search.replace("**", "*")

            log.debug("Final search: {}".format(search))

            # this option sorts Sids - # TODO profile
            children = sorted(Finder().find(search, as_sid=True))
            # children = sorted(list(Finder().find(search, as_sid=True)))
            # children = sorted(list(Finder().find(search, as_sid=False)))
            # children = list(filter(bool, [Sid(s) for s in children]))

            parent.setRowCount(len(children))
            for row, sid in enumerate(children):

                # FIXME: hardcoded "p" -> config
                # sid_color = (
                #     sid_colors.get("published")
                #     if sid.get_with(state="p").exists()
                #     else None
                # )
                item = addTableWidgetItem(
                    parent, sid, sid, row=row, column=0  # , fgcolor=sid_color
                )

                for i, func in enumerate(table_bloc_functions):
                    addTableWidgetItem(
                        parent, sid, str(func(sid)) or "", row=row, column=i + 1
                    )

                # log.debug('{} // {} ?'.format(sid, self.search))
                if sid == self.search:
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
        If needed calls clear_versions. (#TODO make this code more readable)
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
        """
        Clears the "versions" table widget (the right part of the central layout)
        """
        self.versions_tw.clear()

    def set_sid_from_history(self):
        """
        Launches a new search when the Sid history (latest used Sids) is changed.
        """
        # TODO: implement global history handler
        selected = self.sid_history_cb.itemText(self.sid_history_cb.currentIndex())
        if selected:
            log.debug("selected " + selected)
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
        log.debug(f'Select search: item sid="{sid}", self.search="{self.search}"')

        # "reset" mode
        if self.sender() == self.versions_tw:
            self.launch_search(sid)
        else:
            # "sticky" mode
            sid = Sid(sid)
            key = sid.keytype
            if self.search.type and key not in search_reset_keys:
                # TODO: implement this in the Sid, and document
                # implement option to use # .get_with(key=key, value='~' + sid.get(key))
                search = Sid(str(self.search) + f"?{key}=~{sid.get(key)}")
                self.launch_search(search)
            else:
                # "reset" mode
                self.launch_search(sid)

    def input_search(self):
        """
        Called when the input sid lineEdit "input_sid_le" is triggered.
        Launches a new search.
        """
        log.debug("input_search {}".format(self.input_sid_le.text()))
        self.launch_search(self.input_sid_le.text())

    # TODO: factorize and simplify all the xxx_search methods
    def edit_search(self, search_sid):
        """
        If the search has no searchers ("*", ",", ...) it needs edit.
        """
        # we check this first, because the Sid might not be typed.
        if search_sid.is_search():
            return search_sid

        if is_leaf(search_sid):
            return search_sid

        return Sid(str(search_sid) + "/*")

    def launch_search(self, search_sid):
        """
        Main entry point for a new search.
        Called either by:
        - __init__ (browser start),
        - set_sid_from_history (sid history menu),
        - input_search (search sid line edit), or
        - select_search (click select a sid)

        Launches a new search cycle.
        - instantiates the Sid
        - calls edit_search: add search criterias ('*') if needed.
        - sets self.search
        - sets the input field
        - calls boot_entities: triggers UI update with the new columns, table, buttons
        """
        log.debug("New search cycle: " + str(search_sid))
        search_sid = Sid(search_sid)

        # if it is a leaf (typically a file), we keep the current search as long as it matches
        if is_leaf(search_sid) and search_sid.match(self.search):
            log.debug(
                f'Matching Leaf "{search_sid}". Setting "Current sid", keeping search sid'
            )
            self.current_sid = search_sid
            self.update_current_sid()
            return

        # check if the search needs update
        search_sid = self.edit_search(search_sid)
        self.search = search_sid
        self.input_sid_le.setText(self.search.string)

        self.boot_entities()

    def update_current_sid(self):
        """
        The current Sid is the one selected, seen at the top center of the UI.
        When it is updated, this method updates the Qt label,
        and calls the ActionHandlers update() method.
        """
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
            box.setObjectName("ext_" + ext)
            box.clicked.connect(self.build_versions)
            vbox.addWidget(box)
            self.boxes.append(box)

        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        self.engine_la.addWidget(groupBox)

    # Utils
    def create_entity_widget(self, key):
        """
        Utility to create an Entity column widget list.
        """
        list_widget = QtWidgets.QListWidget()
        list_widget.setObjectName(key)
        self.entities_lo.addWidget(list_widget)
        self.sid_widgets[key] = list_widget
        return list_widget

    def fill_history(self, sid=None):
        """
        Fills the "history" combo box containing last used Sids.

        Appends the given Sid to it, drops least recently used,
        to keep it as configured length.

        Args:
            sid:

        Returns:
        """

        self.sid_history_cb.clear()

        if sid:
            self.sid_history.append(str(sid))
            self.sid_history = uniqfy(self.sid_history, reverse=True)
            if len(self.sid_history) > conf.sid_usage_history_len:
                self.sid_history.pop(0)

            self.sid_history_cb.addItem(str(sid))
        else:
            self.sid_history_cb.addItem("")

        for sid in reversed(self.sid_history):  # history only for current environment ?
            self.sid_history_cb.addItem(str(sid))

    def connect_events(self):
        self.input_sid_le.returnPressed.connect(self.input_search)
        self.sid_history_cb.currentIndexChanged.connect(self.set_sid_from_history)
        self.versions_tw.itemClicked.connect(self.select_search)
        self.last_cb.clicked.connect(self.build_versions)
        self.publish_cb.clicked.connect(self.build_versions)
        self.work_cb.clicked.connect(self.build_versions)
        # QtWidgets.QShortcut(QtCore.Qt.Key_Up, self.centralwidget, self.select_search)  # TODO: arrow keys in listwidgets

    def showEvent(self, arg=None):
        """
        When the window is shown.
        Reads the last used Sid history list from the user config.
        """
        self.sid_history = conf.sid_usage_history  # TODO : test this : no real refresh
        self.fill_history()

    def closeEvent(self, arg=None):
        """
        When the window is closed.
        Persists the last used Sid history list to the user config.
        """
        try:
            conf.set("sid_usage_history", self.sid_history)
        except Exception:
            pass


def open_browser(
    sid: Optional[Sid | str] = None, do_new: Optional[bool] = False
) -> Browser:
    """
    Opens a browser window.
    If the window already exists, brings the existing one to the front.
    If do_new is set to True, a new Window instance is created

    (The Qt Application must already exist)

    Args:
        sid: the ui navigates to the given Sid upon startup
        do_new: if True, opens a new window instance, else brings the existing one to the front (default).

    Returns:
        the Browser window object
    """

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
        browser_window.setWindowState(
            browser_window.windowState() & ~QtCore.Qt.WindowMinimized
            | QtCore.Qt.WindowActive
        )
        browser_window.show()

    return browser_window


def app(sid: Optional[Sid | str] = None) -> None:
    """
    Gets or creates a QApplication instance,
    and opens the Browser window.

    Args:
        sid: Optional Sid instance or String to start with

    """

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)  # fix
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])

    # darkstyle
    import qdarkstyle
    app.setStyleSheet(qdarkstyle.load_stylesheet(palette=qdarkstyle.DarkPalette))
    # app.setStyleSheet(qdarkstyle.load_stylesheet(palette=qdarkstyle.LightPalette))
    # app.setStyleSheet(qdarkstyle.load_stylesheet())

    # profiling
    # import cProfile
    # cProfile.run('open_browser(sid, do_new=True)', sort=1)

    open_browser(sid)
    app.exec_()


if __name__ == "__main__":

    from spil.util.log import DEBUG, setLevel, WARN, ERROR, INFO

    setLevel(ERROR)

    sid = "hamlet/a/char/ophelia"
    app(sid)
