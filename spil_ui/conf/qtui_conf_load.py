"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2023 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""
from typing import Dict
import importlib
import inspect

# stubs that are replaced by imports
is_leaf = None
browser_title = ""
get_action_handler = None
table_bloc_columns = []
table_bloc_functions = []
extension_filters = []
search_reset_keys = []
basetype_to_cut = {}
basetype_clipped_versions = []


try:
    module = importlib.import_module('spil_qtui_conf')
except ModuleNotFoundError as e:
    from spil.conf import sid_conf_import_error_message
    problem = sid_conf_import_error_message.format(module='spil_qtui_conf')
    print(problem)
    raise Exception(problem)

__all__ = []
for name, value in inspect.getmembers(module):
    if name.startswith('__'):
        continue

    globals()[name] = value
    __all__.append(name)


if __name__ == '__main__':

    from pprint import pprint

    pprint(globals())
