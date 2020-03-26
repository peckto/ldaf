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

import importlib.util
import time
import pandas as pd
import sys
import os

import typing
if typing.TYPE_CHECKING:
    from .App import App


def load_module(path: str):
    """Load a Analysis Module from path.
    Path can be external. Path will be added os.path

    :param path: Path to Python file to load
    :return:
    """
    name = os.path.basename(path).split('.')[0]
    spec = importlib.util.spec_from_file_location(name, path)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    sys.modules[name] = foo
    sys.path.append(os.path.dirname(os.path.abspath(path)))
    return foo


def log_time_frame(df: pd.DataFrame, app: 'App'):
    """Log time span fo DataFrame in App logging widget

    :param df: Input DataFrame
    :param app: Application
    :return:
    """
    if 'time' in df.columns:
        t1 = df['time'].min()
        t2 = df['time'].max()
        t1 = time.gmtime(t1)
        t2 = time.gmtime(t2)
        app.log('Time frame: %s - %s' % (time.strftime('%H:%M', t1), time.strftime('%H:%M', t2)))


tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
