"""
With many thanks to https://stackoverflow.com/users/168717/akiross
https://stackoverflow.com/a/28976373

"""

from qtpy.QtWidgets import QLineEdit, QCompleter
from qtpy.QtCore import Qt, QEvent
from qtpy.QtCore import Signal


class MyLineEdit(QLineEdit):
    tabPressed = Signal()
    keyRight = Signal()
    keyLeft = Signal()

    def __init__(self, completer, parent=None):
        super().__init__(parent)
        # self._compl = QCompleter()
        self._compl = completer
        self.tabPressed.connect(self.next_completion)
        self.keyRight.connect(self.key_right)
        self.keyLeft.connect(self.key_left)

    def next_completion(self):
        index = self._compl.currentIndex()
        self._compl.popup().setCurrentIndex(index)
        start = self._compl.currentRow()
        if not self._compl.setCurrentRow(start + 1):
            self._compl.setCurrentRow(0)

    def key_right(self):
        if not self.text().endswith("/"):
            self.setText(self.text() + "/")
        # else:
        #     self.next_completion()

    def key_left(self):
        if self.text().endswith("/"):
            self.setText(self.text().rstrip("/"))
        else:
            self.setText(self.text().rsplit("/", 1)[0])

    def event(self, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.tabPressed.emit()
            return True
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Right:
            # self.keyRight.emit()
            self.key_right()
            return True
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Left:
            self.keyLeft.emit()
            return True
        return super().event(event)
