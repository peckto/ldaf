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

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QDialogButtonBox
import typing
if typing.TYPE_CHECKING:
    from ..App import App


class FeatureSelector(QDialog):
    """Feature selector dialog

    """

    def __init__(self, app: 'App', parent: QDialog, settings: dict):
        super().__init__(parent)
        self.setWindowTitle('Feature Selector')
        self.app = app
        self.settings = dict()

        self.layout = QVBoxLayout()
        for key, value in settings.items():
            txt, en = value
            self.add_checkbox(key, txt, en)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

    def add_checkbox(self, key, name, en=False):
        b = QCheckBox(name)
        self.layout.addWidget(b)
        self.settings[key] = b
        b.setChecked(en)

    def get_selected_features(self):
        l = list()
        for key, value in self.settings.items():
            if value.isChecked():
                l.append(key)

        return l
