"""
With many thanks to https://stackoverflow.com/users/820013/shao-lo
https://stackoverflow.com/a/52570662
"""

import sys
from qtpy.QtWidgets import QApplication, QLineEdit, QWidget, QGridLayout, QCompleter
from qtpy.QtCore import Qt

from ex3 import MyLineEdit


class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setMinimumWidth(420)

        layout = QGridLayout()
        self.setLayout(layout)

        self.completer = QCompleter([])  # Initialze with a list...to establish QStringListModel
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setMaxVisibleItems(10)

        self.lineedit = MyLineEdit(self.completer) # QLineEdit()
        self.lineedit.setCompleter(self.completer)
        self.lineedit.setFixedHeight(30)
        self.lineedit.setFixedWidth(360)
        self.lineedit.textChanged.connect(self.text_changed)
        layout.addWidget(self.lineedit,0,0)


    def get_request(self, line_text):

        import sys
        sys.path.append('/home/mh/PycharmProjects/spilplatz2/spil_hamlet_conf')
        import spil
        from spil import FindInAll, Sid

        print(f'In: {line_text}')

        f = FindInAll()
        found = None

        if not line_text.count("/"):
            search = Sid("*")
            print(search)
            found = list(f.find(search, as_sid=False))

        if line_text.endswith("/"):
            search = Sid(line_text + "*")
            print(search)
            found = ["*", "**"] + sorted(f.find(search, as_sid=False))

        if line_text.endswith("*") or line_text.count("**"):
            search = Sid(line_text)
            print(search)
            found = ["*", "**"] + sorted(list(f.find(search, as_sid=False)))

        print(f'Out: {found}')

        return found


    def text_changed(self):
        #the function get_request returns a list of names taken from
        #a database e.g ['matthew','mark','morris','mickey']
        vals = self.get_request(self.lineedit.text())

        if vals:
            model = self.completer.model()
            model.setStringList(vals)  # Updated the QStringListModel string list


app = QApplication(sys.argv)

screen = Window()
screen.show()

sys.exit(app.exec_())