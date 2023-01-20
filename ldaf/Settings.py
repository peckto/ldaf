# Copyright (C) 2023 Tobias Specht
# This file is part of ldaf <https://github.com/peckto/ldaf>.
#
# ldaf is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ldaf is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ldaf.  If not, see <http://www.gnu.org/licenses/>.

from PyQt5.QtWidgets import QTableWidgetItem, QComboBox
from PyQt5.Qt import Qt

import typing
if typing.TYPE_CHECKING:
    from .App import App


class Settings(object):
    """Class representing the Seeings Widget in the UI.
    A setting is a key, value pair.
    Settings can be created and the value can be read.

    """
    def __init__(self):
        self.args = dict()

        self.app: 'App' = None
        "reference to QT Application, will be initialised by App"

    def settings_add_combo_box(self, name: str, values: list, func=None):
        """add Combo Box (Drop Down) to settings

        :param name: name of setting
        :param values: values fot Combo Box
        :param func: callback for onChange event
        :return:
        """
        row = self.app.tableWidget.rowCount()
        self.app.tableWidget.insertRow(row)
        self.app.tableWidget.setItem(row, 0, QTableWidgetItem(name))
        cb = QComboBox()
        if func is not None:
            cb.currentIndexChanged.connect(func)
        self.app.tableWidget.setCellWidget(row, 1, cb)
        if values:
            cb.addItems(values)

        return cb

    def settings_add_check_box(self, name: str, value: bool = False, func=None):
        """add check box to settings

        :param name: name of setting
        :param value: init value for check box
        :param func: callback for onChange event
        :return:
        """
        row = self.app.tableWidget.rowCount()
        self.app.tableWidget.insertRow(row)
        self.app.tableWidget.setItem(row, 0, QTableWidgetItem(name))
        cb = QTableWidgetItem()
        cb.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        if value:
            cb.setCheckState(Qt.Checked)
        else:
            cb.setCheckState(Qt.Unchecked)

        if func is not None:
            cb.currentIndexChanged.connect(func)

        self.app.tableWidget.setItem(row, 1, cb)

        return cb

    def add_settings(self):
        """callback to add custom settings

        """
        raise NotImplementedError

    def set_setting(self, k: str, v: str):
        """Create new setting on widget

        :param k: setting name, key
        :param v: setting default value
        :return:
        """
        rows = self.app.tableWidget.rowCount()
        for i in range(0, rows):
            e = self.app.tableWidget.item(i, 0).text()
            if e == k:
                self.app.tableWidget.setItem(i, 1, QTableWidgetItem(v))
                return

        self.app.tableWidget.insertRow(rows)
        self.app.tableWidget.setItem(rows, 0, QTableWidgetItem(k))
        self.app.tableWidget.setItem(rows, 1, QTableWidgetItem(v))

    def get_settings(self):
        """Read settings from Widget and store then in internal state

        :return:
        """
        rows = self.app.tableWidget.rowCount()
        for i in range(0, rows):
            e = self.app.tableWidget.item(i, 0).text()
            v = self.app.tableWidget.cellWidget(i, 1)
            if v is None:
                v = self.app.tableWidget.item(i, 1)
                ret = v.flags() & Qt.ItemIsEditable
                if not ret:
                    v = bool(v.checkState())
                else:
                    v = v.text()
                    if v.isnumeric():
                        v = int(v)

            elif isinstance(v, QComboBox):
                v = v.currentText()
            else:
                print('[+] Warning: unsupported table widget: %s' % v)
                continue

            self.set(e, v)

    def get(self, key):
        """Read setting by key

        :param key: setting key to read
        :return:
        """
        self.get_settings()

        if key not in self.args:
            return None
        return self.args[key]

    def set(self, key, value):
        """Update setting

        :param key: setting key
        :param value: new value
        :return:
        """
        self.args[key] = value
