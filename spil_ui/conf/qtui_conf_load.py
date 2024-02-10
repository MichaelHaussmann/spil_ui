"""
This file is part of spil_ui, a UI using SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2024 Michael Haussmann, spil@xeo.info

SPIL is free software and is distributed under the MIT License. See LICENCE file.
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
