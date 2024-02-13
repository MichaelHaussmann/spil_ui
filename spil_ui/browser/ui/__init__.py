# -*- coding: utf-8 -*-
"""
This file is part of spil_ui, a UI using SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2024 Michael Haussmann, spil@xeo.info

SPIL is free software and is distributed under the MIT License. See LICENCE file.
"""

from spil import conf
from spil_ui.conf import sid_usage_history_len

# print('INIT BROWSR package')

if not conf.get('sid_usage_history'):
    conf.set('sid_usage_history', [])

if not conf.get('sid_usage_history_len'):
    conf.set('sid_usage_history_len', sid_usage_history_len)