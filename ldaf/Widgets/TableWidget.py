# Copyright (C) 2020 Tobias Specht
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

from PyQt5.QtWidgets import QTableWidget, QMenu


class TableWidget(QTableWidget):
    """Custom QTableWidget with context menu event

    """
    def __init__(self, mod, parent=None):
        QTableWidget.__init__(self, parent)
        self.mod = mod

    def contextMenuEvent(self, event):
        index = self.indexAt(event.pos())
        row = index.row()
        col = index.column()
        header = self.horizontalHeaderItem(col).text()
        item = self.item(row, col).text()
        if header in self.mod.window.tableActions.keys():
            d = dict()
            menu = QMenu(self)
            for mod, txt, f in self.mod.window.tableActions[header]:
                d[menu.addAction(txt)] = f
            action = menu.exec_(self.mapToGlobal(event.pos()))
            if action in d.keys():
                self.mod.window.set_setting(header, item)
                d[action](item)
