# Spil UI

Spil UI is part of [Spil, the Simple Pipeline Lib](https://github.com/MichaelHaussmann/spil).

It ships a dynamic Sid Browser and Action launcher.

[![Spil Qt UI](https://raw.githubusercontent.com/MichaelHaussmann/spil_ui/main/docs/img/spil_ui_dark.png?token=GHSAT0AAAAAACT3SBZGNFHI6PANN2SOK7BOZUEMPLA)](https://github.com/MichaelHaussmann/spil_ui)

The **Browser** finds Sids (Scene IDs) using Spil's `Finder` classes.  
It is dynamic, and adapts to the Sids length and content.  

Spil UI also includes a simple Sid Search Bar. 

![Spil Qt UI Bar](https://raw.githubusercontent.com/MichaelHaussmann/spil_ui/main/docs/img/bar.png?token=GHSAT0AAAAAACT3SBZGJFFV3ZPHHFN22AMAZUEMTYQ)

The **Bar** allows quick keyboard navigation by using tab and arrow keys.

Both UIs is built using [QtPy](https://github.com/spyder-ide/qtpy), and [QDarkStyle](https://github.com/ColinDuquesnoy/QDarkStyleSheet), and work with PyQt5, PySide2, PyQt6, PySide6.
(Spil works with python >=3.7)

They runs on all major DCCs as well as standalone. It was tested in Maya, Houdini, Nuke, and others.

ActionHandlers can be implemented to show and call actions matching the selected Sid.    
An example ActionHandler is included (with "explore" and "open" actions).


## Documentation

To lean more about **spil**, please visit [spil.readthedocs.io](https://spil.readthedocs.io)

Usage documentation of **spil_ui**: [Usage](docs/usage.md).

Technical overview of **spil_ui**: [Tech Notes](docs/notes.md).

## Installation

spil_UI can be pip installed.

```shell
pip install spil_ui
```
It installs `spil_ui`, `spil` and its dependencies.  
It also installs `spil_hamplet_conf`, a sample configuration.   

A Qt package must be installed separately.    
Any [QtPy](https://github.com/spyder-ide/qtpy) compatible Qt version: PySide2, PySide6, PyQt5, or PyQt6.  
  
```shell
pip install PySide2
```

### Running

Initialize demo files and folders from the sample configuration: 
```python
import spil  # adds spil_hamlet_conf to the python path
import hamlet_scripts.save_examples_to_mock_fs as mfs
mfs.run()
```

Then you can run the app.
```python
from spil_ui import app
app()
```

From within a DCC already running a QApplication Instance, run:
```python
from spil_ui import open_browser
open_browser()
```

## Limitations

Although it has been and is used in production, the current version of spil_ui is quite rudimentary.
It is work in progress. There are still hard coded elements in the browser.
General code cleanup is planned (typing, tests, etc.).

Spil_UI has been released as early beta to help demonstrate the usage of Spil.

### Todo

- code: cleanup, documentation, typing, formatting (apologies to you reader)
- window opening size and position, better default, and store for user
- stylesheet & choice of light/dark
- tab order (and arrows left/right) for mouseless navigation
- arrow keys (up/down) in listwidgets
- last action in conf for double click / default action
- double-click "unsticks"
- actions refresh browser when done
- use Getter to show images

## Contact

Don't hesitate to get in touch : [spil@xeo.info](mailto:spil@xeo.info).  
We will be happy to respond.  

**spil_ui** is released under MIT licence.

<br>

*This documentation is work in progress.*
