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

    alias("browser", 'python -c "from spil_ui import app;app()"')
    alias("bar", 'python -c "from spil_ui import bar;bar()"')


is_pure_python = True
