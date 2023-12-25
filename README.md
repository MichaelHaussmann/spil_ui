# Spil UI

Spil UI is part of [Spil, the Simple Pipeline Lib](https://github.com/MichaelHaussmann/spil).

It is a simple Qt UI to browse Sids (Scene IDs) using Spil's `Finder` classes.
It is dynamic, and adapts to the Sids length and content.

ActionHandlers can be implemented to show and call actions matching the selected Sid.
An example ActionHandler is included.

[![Spil Qt UI](https://raw.githubusercontent.com/MichaelHaussmann/spil/main/docs/img/spil_ui.png)](https://github.com/MichaelHaussmann/spil_ui)

The UI is built using [QtPy](https://github.com/spyder-ide/qtpy), and works with PyQt5, PySide2, PyQt6, PySide6.
(Spil works with python >=3.7)

It runs on all major DCCs as well as standalone. It was tested in Maya, Houdini, Nuke, and others.

To lean more, please visit [spil.readthedocs.io](https://spil.readthedocs.io)


## ActionHandlers

The ActionHandler is a way to add actions to the Browser.
On each Sid selection in the browser, the ActionHandler's update method is called, with the given selection.
The handler can then accordingly construct buttons and other features.

The ActionHandler can be run as a standalone for testing:  
[![Example ActionHandler Standalone](https://raw.githubusercontent.com/MichaelHaussmann/spil_ui/main/docs/img/action_handler_stdalone.png)]


## Limitations

Although it has been and is used in production, the current version of spil_ui is quite rudimentary.
It is still work in progress. General code cleanup is planned (typing, tests, etc.).

Although it is usable (and used), there are still hard coded elements in the browser.
It has been released as early beta to help demonstrate the usage of Spil.

**This documentation is work in progress.**
