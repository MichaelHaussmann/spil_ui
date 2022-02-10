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
The ActionHandler is a way to add actions to the Browser.

On each Sid selection in the browser, the ActionHandler's update method is called, with the given selection.

The handler can then accordingly construct buttons and other features.

The ActionHandler can be run as a standalone, like in the main.

"""
# Uses Qt.py
from Qt import QtWidgets
from spil_ui.util.dialogs import Dialogs

from spil import logging, SpilException
log = logging.get_logger("action_handler")


class AbstractActionHandler(object):

    def init(self, parent_window, parent_widget, callback=None):
        pass

    def update(self, selection):
        pass

    def __str__(self):
        return self.__class__.__name__


class ExampleActionHandler(AbstractActionHandler, QtWidgets.QWidget):  # inherits QWidget to have a sender() on button clic

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

        self.action_box.setTitle('Actions')
        for b in self.buttons:
            b.setVisible(False)
            b.deleteLater()
        self.buttons = []

        for action in self.get_actions_by_sid(self.selection):
            button = QtWidgets.QPushButton(action, self.parent_window)
            # button.setToolTip((getattr(self.engine, action.get("name")).__doc__ or '').strip().replace('\t', ''))
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
            self.uio.error('Could not call "{0}" with "{1}".\nError : {2}'.format(sender, sid, e))

        except SpilException as e:
            self.uio.error('{0}'.format(e))

    def runner(self, action, selection):
        msg = 'Now running {} on "{}"'.format(action, selection)
        log.info(msg)
        self.uio.inform(msg)

    def get_actions_by_sid(self, selection):
        return ['ExampleA', 'ExampleB']


if __name__ == '__main__':

    # Running the ActionHandler without the Browser UI

    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])

    action_ui = ExampleActionHandler()
    action_ui.init(action_ui, QtWidgets.QGridLayout())
    action_ui.update('FTOT')
    action_ui.show()
    action_ui.update('FTOT/A/CHR/TITI')
    action_ui.show()
    app.exec_()
