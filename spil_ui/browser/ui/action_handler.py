# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""

"""
The ActionHandler is a way to add actions to the Browser.

On each Sid selection in the browser, the ActionHandler's update method is called, with the given selection.

The handler can then accordingly construct buttons and other features.

The ActionHandler can be run as a standalone for testing (as in this main).

"""
# Uses Qt.py
from Qt import QtWidgets
from spil_ui.util.dialogs import Dialogs

from spil import Sid, SpilException, logging

log = logging.get_logger("action_handler")
log.setLevel(logging.INFO)


class AbstractActionHandler(object):
    """
    During startup, the Browser ask the configuration for an ActionHandler object.

    The ActionHandler is typically a QtWidget that gets inserted into the Browser window,
    and that interacts with it.
    The goal is to be able to execute Actions on selected Sids.

    The process is:
    - The configuration instantiates an ActionHandler and returns it to the Browser.
    - Browser calls the ActionHandler.init() and passes itself, the self.central_layout, and a callback function.
    - on each Sid update (new Sid selection), the Browser calls ActionHandler.update() and passes the selected Sid.
    - the ActionHandler can call the callback, optionally passing a Sid.

    The ActionHandler implements Buttons (and potentially other Qt Widgets),
    and handles the Button pushes and action execution.
    The Browser only serves for browsing.
    """

    def init(self, parent_window, parent_widget, callback=None):
        """
        During Browser startup, it calls this init method.
        It passes itself (the Browser instance), it's central_layout, and a callback function.

        Args:
            parent_window: the Browser instance
            parent_widget: the Browser's central layout
            callback: a function to call on each action execution

        Returns:
            None

        """
        pass

    def update(self, selection: Sid) -> None:
        """
        Update is called by the browser each time a new Sid is selected.

        Args:
            selection: selected Sid instance

        Returns:
            None
        """
        pass

    def __str__(self):
        return self.__class__.__name__


class ExampleActionHandler(AbstractActionHandler, QtWidgets.QWidget):
    # inherits QWidget to have a sender() on button clic
    """
    Example ActionHandler.

    Implements a series of Buttons, as defined in example_actions.
    Buttons call a function using the selected Sid.
    """

    def __init__(self):
        super(ExampleActionHandler, self).__init__()
        self.uio = Dialogs()
        self.selection = None
        self.buttons = []

    def init(self, parent_window, parent_widget, callback=None):
        self.parent_window = parent_window
        self.action_box = QtWidgets.QGroupBox("Actions", parent_window)
        self.action_layout = QtWidgets.QHBoxLayout(parent_window)
        self.action_box.setLayout(self.action_layout)
        parent_widget.addWidget(self.action_box)
        self.callback = callback

    def update(self, selection):

        self.selection = selection

        self.action_box.setTitle("Actions")
        for b in self.buttons:
            b.setVisible(False)
            b.deleteLater()
        self.buttons = []

        actions = self.get_actions_by_sid(self.selection)
        for action in actions:
            button = QtWidgets.QPushButton(action, self.parent_window)
            button.setToolTip(
                (actions.get(action).__doc__ or "").strip().replace("\t", "")
            )
            button.setObjectName(action)
            button.clicked.connect(self.run_actions)
            self.action_layout.addWidget(button)
            self.buttons.append(button)

    def run_actions(self):  # TODO: more advanced features with parameters or options

        if not self.selection:
            return

        sid = self.selection

        sender = self.sender().objectName()

        log.debug('sender: ["{0}"]'.format(sender))

        try:
            self.runner(sender, sid)
            if self.callback:
                self.callback(sid)

        except RuntimeError as e:
            self.uio.error(f'Could not call "{sender}" with "{sid}".\nError : {e}')

        except SpilException as e:
            self.uio.error(f"{e}")

    def runner(self, action, selection):
        msg = f'Now running {action} on "{selection}"'
        log.info(msg)
        func = self.get_actions_by_sid(selection, action)
        func(selection)
        # self.uio.inform(msg)

    @staticmethod
    def get_actions_by_sid(selection, action=None):

        from spil_ui.conf.example_actions import get_action_for_sid

        actions = get_action_for_sid(selection)

        if action:
            return actions.get(action)
        else:
            return actions


if __name__ == "__main__":

    # Running the ActionHandler without the Browser UI

    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])

    action_ui = ExampleActionHandler()
    action_ui.init(action_ui, QtWidgets.QGridLayout())

    test = Sid("hamlet")
    action_ui.update(test)
    action_ui.show()

    test2 = Sid("hamlet/a/char/ophelia/model/v001/p/ma")
    action_ui.update(test2)
    action_ui.show()

    app.exec_()
