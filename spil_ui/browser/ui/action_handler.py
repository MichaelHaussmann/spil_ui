"""
This file is part of spil_ui, a UI using SPIL, The Simple Pipeline Lib.

(C) copyright 2019-2024 Michael Haussmann, spil@xeo.info

SPIL is free software and is distributed under the MIT License. See LICENCE file.
"""
from spil import Sid
"""
The ActionHandler is a way to add actions to the Browser.
On each Sid selection in the browser, the ActionHandler's update method is called, with the given selection.
The handler can then accordingly construct buttons and other features.
See example implementation in the demo config.
"""


class AbstractActionHandler(object):
    """
    During startup, the Browser ask the configuration for an ActionHandler object.

    The ActionHandler is typically a QtWidget that gets inserted into the Browser window,
    and that interacts with it.
    The goal is to be able to execute Actions on selected Sids.

    The process is:
    - The configuration instantiates an ActionHandler and returns it to the Browser.
    - Browser calls the ActionHandler.init() and passes itself, the self.central_layout, and a callback function.
    - on each Sid update (new Sid selection), the Browser calls ActionHandler.update() and passes the selected Sid.
    - the ActionHandler can call the callback, optionally passing a Sid.

    The ActionHandler implements Buttons (and potentially other Qt Widgets),
    and handles the Button pushes and action execution.
    The Browser only serves for browsing.
    """

    def init(self, parent_window, parent_widget, callback=None):
        """
        During Browser startup, it calls this init method.
        It passes itself (the Browser instance), it's central_layout, and a callback function.

        Args:
            parent_window: the Browser instance
            parent_widget: the Browser's central layout
            callback: a function to call on each action execution

        Returns:
            None

        """
        pass

    def update(self, selection: Sid) -> None:
        """
        Update is called by the browser each time a new Sid is selected.

        Args:
            selection: selected Sid instance

        Returns:
            None
        """
        pass

    def __str__(self):
        return self.__class__.__name__
