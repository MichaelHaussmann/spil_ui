"""
With many thanks to https://stackoverflow.com/users/168717/akiross
https://stackoverflow.com/a/28976373

"""

from qtpy.QtWidgets import QLineEdit
from qtpy.QtCore import Qt, QEvent


class EventLineEdit(QLineEdit):
    """
    QLineEdit implementing events to navigate the autocompletion data.

    tabPressed => next completion
    keyRight => adds "/" (does not work properly, because it does not update the size of the bar)

    """

    def __init__(self, completer, parent=None):
        super().__init__(parent)
        # self._compl = QCompleter()
        # self.bar = parent
        self._compl = completer

    def next_completion(self):
        index = self._compl.currentIndex()
        self._compl.popup().setCurrentIndex(index)
        start = self._compl.currentRow()
        if not self._compl.setCurrentRow(start + 1):
            self._compl.setCurrentRow(0)

    def key_right(self):
        if not self.text().endswith("/"):
            self.setText(self.text() + "/")
            # self.bar.text_changed()  # does not work
        # else:
        #     self.next_completion()

    def key_left(self):
        if self.text().endswith("/"):
            self.setText(self.text().rstrip("/"))
        else:
            self.setText(self.text().rsplit("/", 1)[0])

    def event(self, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.next_completion()
            return True
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Right:
            self.key_right()
            return True
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Left:
            self.key_left()
            return True
        return super().event(event)
