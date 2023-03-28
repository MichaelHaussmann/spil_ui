# Spil UI

Spil UI is part of [Spil, the Simple Pipeline Lib](https://github.com/MichaelHaussmann/spil).

It is a simple Qt UI to browse Sids (Scene IDs) using spils `Finder` classes.
It is dynamic, and adapts to the Sids length and content.

ActionHandlers can be implemented to show and call actions matching the selected Sid.
An example ActionHandler is included.

[![Spil Qt UI](https://raw.githubusercontent.com/MichaelHaussmann/spil/dev/docs/img/spil_ui.png)](https://github.com/MichaelHaussmann/spil_ui)

The UI is built using Qt.py, and works with PySide2 / Qt5.
(Spil works with python >=3.7)

It runs on all major DCCs as well as standalone. It was tested in Maya, Houdini, Nuke, and others.

Although it has been and is used in production, the current version is quite rudimentary.
General code cleanup is planned (typing, better configuration, etc.).

To lean more, please visit [spil.readthedocs.io](https://spil.readthedocs.io)