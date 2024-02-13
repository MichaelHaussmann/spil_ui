"""
This file is part of spil_ui, a UI using SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2024 Michael Haussmann, spil@xeo.info

SPIL is free software and is distributed under the MIT License. See LICENCE file.
"""
from spil import log
from spil.util.caching import lru_kw_cache as cache
from spil_ui.util.time_tools import toHumanReadableLapse


@cache
def get_time(sid, human=True):
    """
    Returns the timestamp of the given sids file, or 0.
    If "human" is True, returns a human-readable format (until second).
    """
    path = sid.path()
    if path:
        result = path.stat().st_mtime
    else:
        result = 0
    if human:
        if result:
            result = toHumanReadableLapse(result)
        else:
            result = "--"

    return result


@cache
def get_size(sid, human=True):

    path = sid.path()
    size = 0
    try:
        size = path.stat().st_size
    except Exception as ex:
        log.debug(ex)

    if human:
        size = "{0:9.2f} Mo".format((float(size) / (1024 * 1024)))

    return size
