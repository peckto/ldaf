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

import pandas as pd

import typing
if typing.TYPE_CHECKING:
    from .App import App


class DataSource(object):
    """Class to store all Data

    """
    def __init__(self):
        self.dfs = dict()
        self.args = dict()
        self.tables = list()

        self.app: 'App' = None
        "reference to QT Application, will be initialised by App"

    def load_data(self):
        """Main Function: load data

        """
        raise NotImplementedError

    def on_tab_change(self, i=0):
        """Callback when Analyzer Tab as been changed.
        Use eg. to update settings, statistics, ...

        """
        raise NotImplementedError

    def get_loaded_tables(self) -> list:
        """return loaded data tables (eg. self.dfs.keys())

        :return:
        """
        raise NotImplementedError

    def get_table_shape(self, table: str) -> tuple:
        """return shape of table (eg. self.dfs[table].shape)

        :param table: table name
        :return:
        """
        raise NotImplementedError

    def get_table(self, name: str) -> pd.DataFrame:
        """get loaded table by name, eg DataFrame

        """
        return self.dfs[name]

    def info(self):
        """Print statistics about loaded tables on stdout

        :return:
        """
        print('Data Frames:')
        for key in self.tables:
            value = None
            if key in self.dfs.keys():
                value = self.dfs[key]
            if isinstance(value, type(None)):
                print('\t* %s: None' % key)
            else:
                print('\t* %s: %s elements' % (key, value.size))

        print('Variables:')
        for key, value in self.args.items():
            print('\t* %s: %s' % (key, value))
