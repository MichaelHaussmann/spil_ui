from __future__ import annotations
from typing import Optional
from qtpy.QtWidgets import QApplication, QWidget, QComboBox
from qtpy import QtCore, QtWidgets, QtGui
from superqt import QSearchableComboBox, QSearchableListWidget

content = [
    ['hamlet'],
    ['a', 's'],
    ['char', 'prop', 'set', 'fx']
]


class Bar(QtWidgets.QMainWindow):

    def __init__(self, search=None):
        super(Bar, self).__init__()
        self.setWindowTitle(f"Spil Bar")

        self.left = 200
        self.top = 200
        self.width = 360
        self.height = 30
        self.initUI()

    def initUI(self):

        self.setGeometry(self.left, self.top, self.width, self.height)
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        # self.cb = QComboBox(self.widget)
        # self.cb.addItem("C")
        # self.cb.addItem("C++")
        # self.cb.addItems(["Java", "C#", "Python"])
        # self.cb.currentIndexChanged.connect(self.selectionchange)
        # self.cb.move(300, 70)

        self.cb = QSearchableComboBox(self)
        self.cb.addItems(
            ["hamlet/a/char", "hamlet/a/prop", "hamlet/a/set", "hamlet/s/s010", "hamlet/s/s020", "hamlet/s/s030"])
        self.cb.move(300, 70)
        self.cb.resize(360, 30)

def open_bar(do_new: Optional[bool] = False) -> Bar:
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
        bar_window = Bar()
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


def app() -> None:
    """
    Gets or creates a QApplication instance,
    and opens the Bar window.

    Args:
        sid: Optional Sid instance or String to start with

    Returns:

    """

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)  # fix
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])

    # darkstyle
    # import qdarkstyle
    # app.setStyleSheet(qdarkstyle.load_stylesheet(palette=qdarkstyle.DarkPalette))

    # profiling
    # import cProfile
    # cProfile.run('open_bar(do_new=True)', sort=1)

    open_bar()
    app.exec_()


if __name__ == "__main__":

    app()
    