# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2024 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""


from qtpy import QtCore, QtWidgets

UserRole = QtCore.Qt.UserRole

table_css = """
QTableView::item { padding: 10px; margin: 2px; border: 0px; }
QTableView::item:selected {
        padding: 10px; margin: 2px;
        border: 0px;
        color: black;
        border-color: transparent;
        background-color: orange;
        }
QTableView::item:focus{ border: 0px; border-color: transparent; padding: 0px; margin: 2px; }
"""


def addTableWidgetItem(parent, sid, label, row, column=1, fgcolor=None):
    item = QtWidgets.QTableWidgetItem()
    item.setData(UserRole, sid)
    item.setText(str(label))
    parent.setItem(row, column, item)
    # item.setStyleSheet("QTableWidget::item { padding: 50px; border: 5px; }")
    if fgcolor:
        item.setForeground(fgcolor)
    return item


def addListWidgetItem(listWidget, data, label):
    """Used to fill a UI listWidget with listWidgetItem (label + data)"""
    item = QtWidgets.QListWidgetItem()
    item.setData(UserRole, data)
    item.setText(label)
    listWidget.addItem(item)
    return item


def clear_layout(layout):
    for i in reversed(range(layout.count())):
        widgetToRemove = layout.itemAt(i).widget()
        layout.removeWidget(widgetToRemove)  # remove it from the layout list
        widgetToRemove.deleteLater()  # remove it from the gui  # setParent(None)


def get_layout_widgets(layout):
    return (layout.itemAt(i) for i in range(layout.count()))
