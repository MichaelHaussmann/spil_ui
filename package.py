# -*- coding: utf-8 -*-

name = 'spil_ui'

version = '0.1.2'

requires = [
    "spil",
    "qtpy",
    "QDarkStyle"
]


description = "https://github.com/MichaelHaussmann/spil_ui"

authors = ['Michael Haussmann']


def commands():
    env.PYTHONPATH.append('{root}')

    alias("browser", 'python -c "import sys;from spil import Sid;sid=Sid(sys.argv[-1]);from spil_ui import app;app(sid or None)"')
    alias("bar", 'python -c "import sys;from spil import Sid;sid=Sid(sys.argv[-1]);from spil_ui import bar;bar(sid or None)"')


is_pure_python = True
