# -*- coding: utf-8 -*-

name = 'spil_ui'

version = '0.0.5'

requires = [
    "spil",
    "qtpy",
    "QDarkStyle"
]


description = "https://github.com/MichaelHaussmann/spil_ui"

authors = ['Michael Haussmann']


def commands():
    env.PYTHONPATH.append('{root}')


is_pure_python = True
