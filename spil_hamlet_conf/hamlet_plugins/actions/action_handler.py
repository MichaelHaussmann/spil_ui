"""
This file is part of spil_ui, a UI using SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2024 Michael Haussmann, spil@xeo.info

SPIL is free software and is distributed under the MIT License. See LICENCE file.
"""

"""
The ActionHandler is a way to add actions to the Browser.
On each Sid selection in the browser, the ActionHandler's update method is called, with the given selection.
The handler can then accordingly construct buttons and other features.
The ActionHandler can be run as a standalone for testing (as in this main).
"""
# Uses QtPy
from qtpy import QtWidgets

from spil_ui.browser.ui.action_handler import AbstractActionHandler
from spil_ui.util.dialogs import Dialogs

from spil import Sid, SpilException, logging

log = logging.get_logger("action_handler")
log.setLevel(logging.INFO)


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
            button = QtWidgets.QPushButton("&" + action, self.parent_window)
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

        from hamlet_plugins.actions.example_actions import get_action_for_sid  # fmt: skip
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
