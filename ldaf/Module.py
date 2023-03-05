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

import importlib.util
import traceback
import functools
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidgetItem, QHeaderView, QLabel
from PyQt5.Qt import Qt
import matplotlib
matplotlib.use('QT5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.style
import matplotlib.offsetbox

matplotlib.style.use('ggplot')
import pandas as pd

from .Widgets.TableWidget import TableWidget
from .helper import load_module

import typing
if typing.TYPE_CHECKING:
    from .App import App


class Module(object):
    """Container Class to store Analysis functions grouped as Module
    Represented in UI inside TabWidget

    """

    def __init__(self, window: 'App', module_path: str):
        """

        """
        print('[+] loading module %s' % module_path)
        self.window = window
        self.mod = load_module(module_path)
        self.tab = QWidget(window)
        self.tabIndex = window.tabWidget.addTab(self.tab, self.mod.name)
        self.figure = plt.gcf()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self.tab)
        self.layoutV = QVBoxLayout()
        self.layoutH = QHBoxLayout()
        self.layoutCheck = QHBoxLayout()
        self.layoutV.addLayout(self.layoutH)
        self.funcButtons = list()
        self.add_functions()
        self.layoutV.addWidget(self.toolbar)
        self.layoutV.addWidget(self.canvas)
        self.tab.setLayout(self.layoutV)

        self.table = TableWidget(self, self.tab)
        self.table.hide()
        self.tableTitle = QLabel()
        self.tableTitle.hide()
        newfont = QFont("Noto Sans", 15, QFont.Bold)
        self.tableTitle.setFont(newfont)
        self.tableTitle.setAlignment(Qt.AlignCenter)
        self.layoutV.addWidget(self.tableTitle)
        self.layoutV.addWidget(self.table)

        self.layoutV.addLayout(self.layoutCheck)

        self.menu = None

        self.handler = None
        'Matplotlib mpl_connect handler'

        self.handler_f = None
        "Matplotlib picker handler function"

        for k, v in self.mod.actions.items():
            if k not in self.window.tableActions.keys():
                self.window.tableActions[k] = [[self, v[0], v[1]]]
            else:
                self.window.tableActions[k].append([self, v[0], v[1]])

        self.window.settings.get_settings()

    def add_functions(self):
        """Add all module Functions as Buttons to UI

        :return:
        """
        keys = list(self.mod.functions.keys())
        keys.sort()
        for n in keys:
            f = self.mod.functions[n]
            b = QPushButton(n, self.window)
            b.clicked.connect(functools.partial(self.plot, f))
            self.funcButtons.append(b)
            self.layoutH.addWidget(b)

    def reload(self):
        """reload Module functions

        :return:
        """
        for b in self.funcButtons:
            self.layoutH.removeWidget(b)
            b.deleteLater()
            del b

        self.reset_canvas()

        importlib.reload(self.mod)
        self.funcButtons = list()
        self.add_functions()

        for key, val in self.mod.settings.items():
            if val is not None:
                self.window.settings.set_setting(key, val)

    def show_table(self, df: pd.DataFrame):
        """View DataFrame as Table

        :param df: DataFrame to show as Table
        :return:
        """
        self.tableTitle.show()
        self.table.show()
        self.tableTitle.setText(df.name)
        self.toolbar.hide()
        self.canvas.hide()
        self.table.clear()
        self.table.setRowCount(0)
        header = df.columns.values
        self.table.setColumnCount(len(header))
        self.table.setHorizontalHeaderLabels(header)
        for index, row in df.iterrows():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for i in range(len(row)):
                self.table.setItem(row_position, i, QTableWidgetItem(str(row[i])))

        header = self.table.horizontalHeader()
        header.setMaximumSectionSize(800)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

    def plot(self, func):
        """Error handling for _plot function

        :param func:
        :return:
        """
        self.window.msgLog.setText('')
        try:
            self._plot(func)
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print(e)
            self.window.msg('Error: %s' % e)
            self.tableTitle.show()
            self.tableTitle.setText('No Data')
            self.table.hide()
            self.toolbar.hide()
            self.canvas.hide()
            self.window.enable()
            return

    def reset_canvas(self):
        if self.handler is not None:
            self.canvas.mpl_disconnect(self.handler)

        self.handler = None
        self.handler_f = None

    def _plot(self, func):
        """Main plotting function
        Supported plots:
        * Matplotlib
        * pandas DataFrame (as Table)

        :param func:
        :return:
        """
        self.window.tabWidget.setCurrentIndex(self.tabIndex)
        self.window.msg('loading diagram...')
        self.window.disable()
        self.window.settings.get_settings()
        self.figure.clear()
        self.reset_canvas()

        gg = func(self.window, fig=self.figure)
        if isinstance(gg, type(None)):
            self.window.msg('ready')
            self.tableTitle.show()
            self.tableTitle.setText('No Data')
            self.table.hide()
            self.toolbar.hide()
            self.canvas.hide()
            self.window.enable()
            return

        if isinstance(gg, pd.DataFrame):
            self.show_table(gg)
            self.window.msg('ready')
            self.window.enable()
            return
        elif gg == 'matplotlib':
            pass
        else:
            print('Error: unknown plot element: %r' % gg)
            return

        if self.handler_f is not None:
            c = self.canvas.mpl_connect('pick_event', self.handler_f)
            self.handler = c

        self.table.hide()
        self.tableTitle.hide()
        self.toolbar.show()
        self.figure.set_canvas(self.canvas)
        self.canvas.show()

        self.figure.tight_layout(pad=5, w_pad=3, h_pad=3)
        self.canvas.draw()

        self.canvas.resize(*self.canvas.get_width_height())
        self.canvas.resize_event()
        self.canvas.updateGeometry()
        self.window.msg('ready')

        self.canvas.draw()
        self.window.enable()
