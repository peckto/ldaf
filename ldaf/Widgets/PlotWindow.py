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

import ggplot
from PyQt5.QtWidgets import QDialog, QVBoxLayout
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import typing
if typing.TYPE_CHECKING:
    from ..App import App


class PlotWindow(QDialog):
    """New plot window

    """

    def __init__(self, app: 'App', parent: QDialog, name='Plot'):
        super().__init__(parent)
        self.app = app
        self.setWindowTitle(name)
        self.ax = None
        self.figure = plt.figure()

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

    def plot(self, gg):
        """Plot a ggplot figure

        :param gg:
        :return:
        """
        self.figure.clear()

        if isinstance(gg, ggplot.ggplot):
            gg.fig = self.figure
            gg.plt = self.figure
            gg.subplots = self.ax
            gg.make()

            self.ax = gg.subplots
            self.figure.set_canvas(self.canvas)
        else:
            return

        self.toolbar.show()
        self.figure.set_canvas(self.canvas)
        self.canvas.show()

        self.figure.tight_layout(pad=5, w_pad=3, h_pad=3)
        self.canvas.draw()

        self.canvas.resize(*self.canvas.get_width_height())
        self.canvas.resize_event()
        self.canvas.updateGeometry()
        self.canvas.draw()

        self.show()
