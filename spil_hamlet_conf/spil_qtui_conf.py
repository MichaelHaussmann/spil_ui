"""
This file is part of spil_ui, a UI using SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2024 Michael Haussmann, spil@xeo.info

SPIL is free software and is distributed under the MIT License. See LICENCE file.
"""
"""
This is the example configuration for spil_ui
"""
from hamlet_plugins.actions.utils import get_size, get_time

sid_usage_history_len = 20
application_name = "Spil"
browser_title = "Browser @ Spil"

# Configuration for the Browser

# Columns that will be shown in the "Versions table".
table_bloc_columns = ["Sid", "Size", "Time"]
# functions that will be called for each Sid, in the same order as the table_bloc_columns.
table_bloc_functions = [get_size, get_time]

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
        from spil_action.libs.ui.action_handler import EngineActionHandler  # fmt: skip
        return EngineActionHandler()

    except Exception as ex:

        from hamlet_plugins.actions.action_handler import ExampleActionHandler  # fmt: skip
        return ExampleActionHandler()
