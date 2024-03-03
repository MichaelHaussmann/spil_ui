"""
This file is part of spil_ui, a UI using SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2024 Michael Haussmann, spil@xeo.info

SPIL_UI is free software and is distributed under the MIT License. See LICENSE file.
"""
from __future__ import annotations
from typing import Optional

"""
With many thanks to https://stackoverflow.com/users/820013/shao-lo
https://stackoverflow.com/a/52570662
"""
# Uses qtpy
from qtpy import QtCore, QtWidgets
from qtpy.QtWidgets import QApplication, QLineEdit, QWidget, QGridLayout, QCompleter
from qtpy.QtCore import Qt

from spil import logging
from spil import FindInAll, Sid
from spil_ui import conf as uiconf

from spil_ui.bar.ui.bar_qt_helper import EventLineEdit

import spil.util.log as sl
sl.setLevel(sl.ERROR)

log = logging.get_logger(name="spil_ui")
log.setLevel(logging.INFO)

class Bar(QWidget):
    """
    The Bar window features a line edit on top of Action Handler Buttons.
    The goal is to browse Sids in a keyboard only way.
    Action Handler Buttons should be equipped with hotkeys, to keep the experience mouse-less.

    The Tab, Arrow-right and Arrow-left keys help speed up the navigation.

    The Bar is still somewhat experimental.
    """

    def __init__(self, search=None):
        QWidget.__init__(self)
        self.setMinimumWidth(420)

        layout = QGridLayout()
        self.setLayout(layout)

        self.completer = QCompleter([])  # Initialze with a list...to establish QStringListModel
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setMaxVisibleItems(10)

        self.lineedit = EventLineEdit(self.completer, self)  # QLineEdit()
        self.lineedit.setCompleter(self.completer)
        self.lineedit.setFixedHeight(30)
        self.lineedit.setFixedWidth(460)
        self.lineedit.textChanged.connect(self.text_changed)
        layout.addWidget(self.lineedit, 0, 0)

        # init sources
        self.action_handler = uiconf.get_action_handler()
        self.action_handler.init(self, layout, callback=self.done_action)
        log.debug(f"Loaded action handler {self.action_handler}")

        self.f = FindInAll()
        if search:
            self.lineedit.setText(search)

    def done_action(self, sid):
        """
        Callback for action handler.
        Currently, does nothing.

        Args:
            sid:
        """
        log.debug(f"Did launch Action on {sid}")

    def get_request(self, line_text):
        """
        For the current line text, retrieves the data for auto completion.
        Builds a search with the current line text, and calls the Sid Finder.

        Args:
            line_text: the current line text

        Returns:
            list of Sid strings

        """

        # print(f'In: {line_text}')

        search = None
        found = None

        if not line_text.count("/"):
            search = Sid("*")
            # print(search)

        # input becomes a search
        if line_text.endswith("/"):

            search = Sid(line_text.rstrip('/'))
            # print(f'search in: {search}')

            key = uiconf.basetype_to_cut.get(search.basetype, "task")
            # print(f'key {key} -> {search.get_as(key)}')
            if search.get_as(key):
                search = search.get_as(key).string + "/**"
            else:
                search = search.string + "/*"

        # elif Sid(line_text):
        #     print(f'Valid: {Sid(line_text)}')
        #     search = Sid(line_text.rstrip('/')).parent

        if str(search):
            # print(f'seach run: {search}')
            found = sorted(self.f.find(search, as_sid=False))

            # FIXME: set single option choice
            if len(found) == 1:
                self.lineedit.setText(found[0])

        # if line_text.endswith("*") or line_text.count("**"):
        #     search = Sid(line_text)
        #     print(search)
        #     found = ["*", "**"] + sorted(list(f.find(search, as_sid=False)))

        # print(f'Out: {found}')

        return found

    def text_changed(self):
        """
        When the line edit text changes, we send the Sid to the action handler,
        and update data for the completer.
        """

        # Send to action handler
        sid = Sid(self.lineedit.text())
        if sid:  # sid.exists()
            self.current_sid = sid
            self.action_handler.update(self.current_sid)
        # else: color in grey #IDEA

        # get data for auto completer
        vals = self.get_request(self.lineedit.text())
        if vals:
            model = self.completer.model()
            model.setStringList(vals)  # Updated the QStringListModel string list


def open_bar(
        sid: Optional[Sid | str] = None, do_new: Optional[bool] = False
) -> Bar:
    """
    Opens a bar window.
    If the window already exists, brings the existing one to the front.
    If do_new is set to True, a new Window instance is created

    (The Qt Application must already exist)

    Args:
        sid: the ui navigates to the given Sid upon startup
        do_new: if True, opens a new window instance, else brings the existing one to the front (default).

    Returns:
        the Bar window object
    """

    global bar_window
    try:
        if not bar_window:
            bar_window = None
    except:
        bar_window = None

    if do_new or not bar_window:
        bar_window = Bar(search=sid)
        bar_window.show()
    else:
        bar_window.activateWindow()
        bar_window.raise_()
        bar_window.setWindowState(
            bar_window.windowState() & ~QtCore.Qt.WindowMinimized
            | QtCore.Qt.WindowActive
        )
        bar_window.show()

    return bar_window


def app(sid: Optional[Sid | str] = None) -> None:
    """
    Gets or creates a QApplication instance,
    and opens the Bar window.

    Args:
        sid: Optional Sid instance or String to start with

    """

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)  # fix
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])

    # darkstyle
    import qdarkstyle
    app.setStyleSheet(qdarkstyle.load_stylesheet(palette=qdarkstyle.DarkPalette))

    # profiling
    # import cProfile
    # cProfile.run('open_bar(sid, do_new=True)', sort=1)

    open_bar(sid)
    app.exec_()


if __name__ == "__main__":

    from spil.util.log import DEBUG, setLevel, WARN, ERROR, INFO

    setLevel(ERROR)

    sid = "hamlet/a/char/ophelia"
    app(sid)
