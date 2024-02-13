"""
This file is part of spil_ui, a UI using SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2024 Michael Haussmann, spil@xeo.info

SPIL is free software and is distributed under the MIT License. See LICENCE file.
"""

try:
    from spil_ui.conf.qtui_conf_load import *
except Exception as e:
    raise Exception('Unable to import the spil_qtui_conf file. \n'
                    'Please check the files compatibility with the latest SPIL version.')
