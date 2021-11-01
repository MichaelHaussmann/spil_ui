# Uses Qt.py
from Qt import QtWidgets
import engines

from spil import logging, SpilException
log = logging.get_logger(name="spil_ui")


def get_action_handler():

    return EngineActionHandler()
    # return AbstractActionHandler()  #


class AbstractActionHandler(object):

    def init(self, parent_window, parent_widget, callback=None):
        pass

    def update(self, selection):
        pass


class EngineActionHandler(AbstractActionHandler, QtWidgets.QWidget):  # inherits QWidget to have a sender() on button clic

    def __init__(self):
        super(EngineActionHandler, self).__init__()
        self.engine = engines.get()
        log.debug('Loaded engine {}'.format(self.engine))
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

        self.action_box.setTitle(self.engine.name.replace('_', ' ').capitalize())
        for b in self.buttons:
            b.setVisible(False)
            b.deleteLater()
        self.buttons = []

        for action in self.engine.get_actions(self.selection):
            button = QtWidgets.QPushButton(action.get("label"), self.parent_window)
            # button.setToolTip((getattr(self.engine, action.get("name")).__doc__ or '').strip().replace('\t', ''))
            button.setObjectName(action.get("name"))
            button.clicked.connect(self.run_actions)
            self.action_layout.addWidget(button)
            self.buttons.append(button)

    def run_actions(self):  # TODO: more advanced features with parameters or options

        if not self.selection:
            return

        sid = self.selection

        sender = self.sender().objectName()

        log.debug('sender: ["{0}"]'.format(sender))

        if sender in self.engine.needs_confirm:
            if not self.uio.warn('This function may alter the scene and is not undoable. Are you sure?', withCancel=True):
                return

        try:
            self.engine.run_action(sender, sid)
            if self.callback:
                self.callback(sid)

        except RuntimeError as e:
            self.uio.error('Could not call "{0}" with "{1}".\nError : {2}'.format(sender, sid, e))

        except SpilException as e:
            self.uio.error('{0}'.format(e))

