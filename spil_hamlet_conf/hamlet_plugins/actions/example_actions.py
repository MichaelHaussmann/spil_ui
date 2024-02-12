"""
This file is part of spil_ui, a UI using SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2024 Michael Haussmann, spil@xeo.info

SPIL is free software and is distributed under the MIT License. See LICENCE file.


This file implements simple functions to be used in the ExampleActionHandler,
to illustrate how it works.
"""
from __future__ import annotations
import subprocess, os, platform
from typing import Callable, Optional

from spil import Sid
from spil import logging

log = logging.get_logger("action_handler")
log.setLevel(logging.INFO)


def get_action_for_sid(sid: Optional[Sid]) -> dict[str, Callable]:
    """
    Returns actions that are available for a given Sid.
    This is just an example to work with the ExampleActionHandler.
    """
    actions = {
        "explore": explore,
    }
    if sid.path() and sid.path().is_file():
        actions["open"] = open
    return actions


def explore(sid: Sid | str) -> bool:
    """
    Opens the Sids parent folder.
    """
    log.debug(f"Expore: {sid}")
    return open(sid, explore=True)


def open(sid: Sid | str, explore: bool = False) -> bool:
    """
    Opens the given Sid's path.
    """
    log.debug(f"Open: {sid} ")
    path = Sid(sid).path()
    if not path:
        log.info(f'Given Sid "{sid}" ("{Sid(sid)}") has no path')
        return False

    if explore and not path.is_dir():
        path = path.parent

    if not path.exists():
        log.info(f'Path does not exist. Path "{path}" for "{sid}" ("{Sid(sid)}")')
        return False

    try:
        resolved = path.resolve()

        if platform.system() == "Darwin":  # macOS
            subprocess.call(("open", resolved))
        elif platform.system() == "Windows":  # Windows
            os.startfile(resolved)
            # subprocess.call(('explorer', resolved))
        else:
            subprocess.call(("xdg-open", resolved))  # linux variants

    except Exception as ex:
        log.error(f'Error in explore: "{path}" for "{sid}" ("{Sid(sid)}"). Error: {ex}')
        return False


if __name__ == "__main__":

    sid = Sid("hamlet/a/char/ophelia/model/v001/p/ma")
    print(sid.exists())
    explore(sid)
    open(sid)
