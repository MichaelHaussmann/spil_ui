# -*- coding: utf-8 -*-
"""
This file is part of spil_ui, a UI using SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2024 Michael Haussmann, spil@xeo.info

SPIL is free software and is distributed under the MIT License. See LICENCE file.

Created on 22 dec. 2011
@author: michael haussmann

"""
# Uses qtpy
from qtpy.QtWidgets import QMessageBox, QApplication, QWidget, QFileDialog, QInputDialog, QLineEdit
from qtpy.QtWidgets import QDialog
from qtpy.QtWidgets import QMainWindow
from qtpy.QtCore import QCoreApplication

from spil_ui.conf import application_name


class conf:
    application_name = application_name


class ChoiceBox(QDialog):
    def __init__(self, choiceA, choiceB, title, windowTitle, parent=None):
        super(ChoiceBox, self).__init__(parent)
        self.msgBox = QMessageBox()
        self.msgBox.setWindowTitle(windowTitle)
        self.msgBox.setText(title)
        self.choiceA = self.msgBox.addButton(choiceA, QMessageBox.YesRole)
        self.choiceB = self.msgBox.addButton(choiceB, QMessageBox.AcceptRole)
        self.cancel = self.msgBox.addButton("Cancel", QMessageBox.RejectRole)
        self.msgBox.show()


class MultiChoiceBox(QDialog):
    def __init__(self, choices, title, windowTitle, parent=None):
        super(MultiChoiceBox, self).__init__(parent)
        self.msgBox = QMessageBox()
        self.msgBox.setWindowTitle(windowTitle)
        self.msgBox.setText(title)

        for choice in choices:
            setattr(self, choice, self.msgBox.addButton(choice, QMessageBox.YesRole))
            # self.choiceA = self.msgBox.addButton(choice, QMessageBox.AcceptRole)

        self.cancel = self.msgBox.addButton("Cancel", QMessageBox.RejectRole)
        # self.cancel = self.msgBox.addButton("Cancel", QMessageBox.RejectRole)
        # self.msgBox.removeButton(self.cancel)

        self.msgBox.show()


class Dialogs(QWidget):
    """
    Implements quick dialog boxes.
    This class' interface is also implemented by the Log module, to allow command line Dialogs handling.
    """

    def __init__(self):
        if not QCoreApplication.instance():
            app = QApplication(sys.argv)
        super(Dialogs, self).__init__()

    def striplog(self, message):
        return str(message).split("] ", 1)[-1]

    def inform(self, message):
        """Opens an information window with a confirm button"""
        QMessageBox.information(
            self,
            conf.application_name,
            QApplication.translate("Dialogs", self.striplog(message), None),
            QMessageBox.Ok,
        )

    def error(self, message):
        """Opens an critical (error) window with a confirm button"""
        QMessageBox.critical(
            self,
            conf.application_name,
            QApplication.translate("Dialogs", self.striplog(message), None),
            QMessageBox.Ok,
        )

    def confirm(self, message, withCancel=False):
        """
        Opens an Yes/No question window and returns a Boolean.
        If withCancel is True, a Cancel button is shown, which triggers a None return.
        """
        if withCancel:
            ret = QMessageBox.warning(
                self,
                conf.application_name,
                QApplication.translate("Dialogs", self.striplog(message), None),
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            )
            if ret == QMessageBox.Yes:
                return True
            if ret == QMessageBox.No:
                return False
            if ret == QMessageBox.Cancel:
                return None
        else:
            ret = QMessageBox.question(
                self,
                conf.application_name,
                QApplication.translate("Dialogs", self.striplog(message), None),
                QMessageBox.Yes | QMessageBox.No,
            )
        return ret == QMessageBox.Yes

    def warn(self, message, withCancel=False):
        """Opens an Ok/Cancel warning window and returns a Boolean"""
        if withCancel:
            ret = QMessageBox.warning(
                self,
                conf.application_name,
                QApplication.translate("Dialogs", self.striplog(message), None),
                QMessageBox.Ok | QMessageBox.Cancel,
            )
        else:
            ret = QMessageBox.warning(
                self,
                conf.application_name,
                QApplication.translate("Dialogs", self.striplog(message), None),
                QMessageBox.Ok,
            )
        return ret == QMessageBox.Ok

    def killer(self, message):
        """Opens an critical (error) window with a confirm button, and kills the application"""
        QMessageBox.critical(
            self,
            conf.application_name,
            QApplication.translate("Dialogs", self.striplog(message), None),
            QMessageBox.Ok,
        )
        sys.exit(f'[Dialogs.killer] System was stopped. "{message}"')

    def getOpenFileName(
        self, message, filter="Images (*.png *.xpm *.jpg);;Text files (*.txt)"
    ):
        # "Images (*.png *.xpm *.jpg);;Text files (*.txt);;XML files (*.xml)"
        result = QFileDialog.getOpenFileName(
            self, self.tr(message), "", self.tr(filter)
        )
        return result[0]

    def getText(self, label="Please enter", default=""):

        # value, boul = QInputDialog.getText(self,  conf.application_name, QApplication.translate("Dialogs", str(label), str(default)))
        value, ok = QInputDialog.getText(
            self, conf.application_name, label, QLineEdit.Normal, default
        )
        return value, ok

    def getTextField(self, label="Please enter", default="", size=(300, 300)):
        dlg = QInputDialog(self)
        dlg.setWindowTitle(conf.application_name)
        dlg.setInputMode(QInputDialog.TextInput)
        dlg.setTextValue(default)
        dlg.setOption(QInputDialog.UsePlainTextEditForTextInput, True)
        dlg.setLabelText(label)
        dlg.resize(*size)
        ok = dlg.exec_()
        return dlg.textValue() if ok else ""

    def choice(self, message, options, default=None):
        """
        Returns the result or False
        """
        index = 0
        if default and default in options:
            index = options.index(default)

        result, ok = QInputDialog.getItem(
            self, conf.application_name, message, options, index
        )
        return str(result) if ok else False

    @staticmethod
    def buttonChoice(choiceA, choiceB, title="", windowTitle=conf.application_name):
        """
        Returns True (choice A), False (choice B) or None (Cancel)
        """
        fxMsgBox = ChoiceBox(choiceA, choiceB, title=title, windowTitle=windowTitle)
        fxMsgBox.msgBox.exec_()

        if fxMsgBox.msgBox.clickedButton() == fxMsgBox.choiceA:
            return True

        if fxMsgBox.msgBox.clickedButton() == fxMsgBox.choiceB:
            return False

        elif fxMsgBox.msgBox.clickedButton() == fxMsgBox.cancel:
            return None

    @staticmethod
    def multiButtonChoice(choices, title="", windowTitle=conf.application_name):
        """
        Returns the index of the choice, starting at 1
        None (Cancel)
        """
        fxMsgBox = MultiChoiceBox(choices, title=title, windowTitle=windowTitle)
        fxMsgBox.msgBox.exec_()

        for choice in choices:
            if fxMsgBox.msgBox.clickedButton() == getattr(fxMsgBox, choice):
                return choices.index(choice) + 1

    def getFromUi(self, ui, getter="sid"):
        """
        Simple little wrapper for UIs to return a value.

        Execs and show() the ui and returns the value from given "getter".

        The function waits for the UI to be closed.
        Works only with Dialogs, not with MainWindows.

        Example:
            from pipe_action.tools.asset.ui import create_asset_ui as cui
            result = Dialogs().getFromUi(ui=cui.CreateAssetUI(sid), getter='result_sid')
        """
        if isinstance(ui, QMainWindow):
            raise Exception(
                f"[Dialogs.getFromUi] The given UI must not be a MainWindow.\nGiven {ui.__class__}"
            )
        try:
            ui.show()
            ui.exec_()
            return getattr(ui, getter)
        except Exception as ex:
            raise Exception(
                '[Dialogs.getFromUi] Unable to get value from ui : "{}"'.format(ex)
            )


if __name__ == "__main__":

    """tests only"""
    import sys

    app = QApplication(sys.argv)

    print("debut")

    """
    from ....tools.asset.ui import create_asset_ui as cui
    sid = 'FTOT/A/*'
    result = Dialogs().getFromUi(ui=cui.CreateAssetUI(sid), getter='result_sid')
    print(result)
    """

    print(Dialogs().getTextField("Please enter a very long text here: ", "...", size=(200, 400)))
    print(Dialogs().getText("Default choice", "Not a bad choice either"))

    # print Dialogs.buttonChoice("Use last saved version", "Use current scene", title="Current scene was modified... what would you like to do?", windowTitle="Tomato")
    print(Dialogs.multiButtonChoice(["Default choice", "Not a bad choice either", "utlimatively best choice"], title="Up to you... \nWhat would you like to do?", windowTitle="Tomato"))

    print(Dialogs().warn("Are you sure you want to start this?"))
    print(Dialogs().choice("choose now between all this crap", ["absolut", "omega", "jack"], "toto"))
    print(Dialogs().choice("choose now between all this crap", ["absolut", "omega", "jack"], "omeg"))
    print(Dialogs().choice("choose now between all this crap", ["absolut", "omega", "jack"], "omega"))

    print(Dialogs().inform("Ok, good answer"))
    print(Dialogs().confirm("Do you like user interfaces?"))
    print(Dialogs().confirm("Do you like user interfaces?", withCancel=True))
    print(Dialogs().error("No, no, no... That was a mistake!"))
    print(Dialogs().getOpenFileName("Ah I forgot... please upload"))
    print(Dialogs().killer("This is the end my friend .... "))
    print("Done")
#     sys.exit(app.exec_())
