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

import importlib
import os.path
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView
from PyQt5.Qt import QTextCursor
import matplotlib
matplotlib.use('QT5Agg')
import matplotlib.style
import matplotlib.offsetbox
matplotlib.style.use('ggplot')

from .MainWindow import Ui_MainWindow
from .DataSource import DataSource
from .Module import Module
from .Settings import Settings
from . import helper

from typing import List


class App(QMainWindow, Ui_MainWindow):
    """Main Application Window

    """

    def __init__(self, app, data_source, modules_dir, settings, title: str = 'LDAF'):
        """

        :type app: QApplication
        :type data_source: DataSource
        :type modules_dir: str
        :type settings: Settings
        """
        Ui_MainWindow.__init__(self)
        QMainWindow.__init__(self)
        settings.app = self
        data_source.app = self

        self.tableActions = {}
        "right clock actions for table view"

        self.app = app
        self.modules_dir = modules_dir
        self.settings = settings
        self.data_source = data_source

        self.setupUi(self)
        self.setWindowTitle(title)

        self.actionLoad_lite.triggered.connect(self.on_load_data)
        self.actionReload_modules.triggered.connect(self.on_reload_modules)
        self.tabs: List[Module] = list()
        "Loaded analysis modules as TabWidget"

        self.load_modules()
        self.settings.add_settings()

        self.active_table = None
        if len(self.tabs) > 0:
            self.active_table = self.tabs[0].mod.table

        self.tabWidget.currentChanged.connect(self.on_tab_changed)

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        header = self.loadedTables.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        for m in self.tabs:
            m.reload()

    def _get_current_module(self) -> Module:
        return self.tabs[self.tabWidget.currentIndex()]

    def _set_current_module(self, x):
        raise NotImplemented

    current_module = property(_get_current_module, _set_current_module)

    def load_modules(self):
        """Load all analysis modules inside modules_dir

        :return:
        """
        ls = os.listdir(self.modules_dir)
        ls.sort()
        for f in ls:
            if f.endswith('.py'):
                m = Module(self, os.path.join(self.modules_dir, f))
                self.tabs.append(m)

    def on_tab_changed(self, i=0):
        """callback on Analysis Tab change

        :param i: new tab index
        :return:
        """
        # reset canvas for all modules to clear callbacks
        for mod in self.tabs:
            mod.reset_canvas()

        self.active_table = self.tabs[i].mod.table
        self.data_source.on_tab_change(i)

    def on_reload_modules(self):
        """callback on reload modules menu action

        :return:
        """
        for mod in self.tabs:
            mod.reload()

        importlib.reload(helper)

    def log(self, msg):
        """Log message to message log widget

        :return:
        """
        self.msgLog.setText('%s\n%s' % (self.msgLog.toPlainText(), msg))
        self.msgLog.moveCursor(QTextCursor.End)

    def msg(self, msg: str):
        """Show message in status bar

        :param msg:
        :return:
        """
        self.statusbar.showMessage(msg)

    def enable(self):
        """Enable application window

        :return:
        """
        self.setEnabled(True)
        self.app.processEvents()

    def disable(self):
        """Disable application window

        :return:
        """
        self.setEnabled(False)
        self.app.processEvents()

    def on_load_data(self):
        """callback on load data menu action

        :return:
        """
        self.msg('loading data...')
        self.disable()
        self.data_source.load_data()
        self.data_source.on_tab_change()
        self.msg('ready')
        self.enable()
        self.update_table_stats()

    def update_table_stats(self):
        """Update statistics about loaded data tables

        :return:
        """
        rows = self.loadedTables.rowCount()
        done = list()
        for i in range(0, rows):
            t = self.loadedTables.item(i, 0).text()
            c = self.loadedTables.item(i, 1)
            if t in self.data_source.dfs.keys():
                c.setText("{:,}".format(self.data_source.dfs[t].shape[0]))
                done.append(t)

        for t in self.data_source.get_loaded_tables():
            if t in done:
                continue

            row_position = self.loadedTables.rowCount()
            self.loadedTables.insertRow(row_position)
            self.loadedTables.setItem(row_position, 0, QTableWidgetItem(t))
            shape = self.data_source.get_table_shape(t)
            self.loadedTables.setItem(row_position, 1, QTableWidgetItem("{:,}".format(shape[0])))
            self.loadedTables.setItem(row_position, 2, QTableWidgetItem("{:,}".format(shape[1])))
