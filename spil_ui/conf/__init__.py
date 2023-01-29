# -*- coding: utf-8 -*-
"""
This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2022 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.
"""

sid_usage_history_len = 20
application_name = "Spil"
browser_title = "Browser @ Spil"

# Configuration for the Browser

table_bloc_columns = ["Sid", "Size", "Time"]
from spil_ui.conf.utils import get_size, get_time
table_bloc_functions = [get_size, get_time]  # functions that will be called for the colums.

# these fields trigger a reset of the search sid - else we are "sticky" and only change the given key.
search_reset_keys = [
    "project",
    "type",
]  # , 'assettype', 'sequence']

# key that separates entity lists (left side) and the version table (right side),
# depending on the search's basetype
basetype_to_cut = {"default": "tasktype"}

# usually, the 'ext' is considered the "leaf" (last) key of a Sid.
# Depending on the basetype, we can override this.
basetype_to_leafkey = {}  # {'render': 'layer'}

# for some search types, the version search gets "clipped", meaning "**" is switched to "*"
# Usefull to handle file sequences by using at the parent folder
basetype_clipped_versions = []  # ['render']

# creates checkboxes to filter file extensions
extension_filters = [
    "maya",
    "hou",
    "blend",
    "movie",
    "cache",
    "img",
    "nk",
]  # 'nk', 'spp'


#  "leaf" means the last key of a Sid. Typically the extension "ext".
#  Can be overridden depending on type.
def is_leaf(sid):
    return sid.is_leaf() or sid.keytype == basetype_to_leafkey.get(sid.basetype, "ext")


# function to return an ActionHandler object
def get_action_handler():
    try:
        # uses the spil action framework
        from spil_action.libs.ui.action_handler import EngineActionHandler

        return EngineActionHandler()
    except Exception as ex:
        from spil_ui.browser.ui.action_handler import ExampleActionHandler

        return ExampleActionHandler()
