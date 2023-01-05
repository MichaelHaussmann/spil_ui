# -*- coding: utf-8 -*-

name = 'spil_ui'

version = '0.0.4'

requires = [
    "spil",
    "Qt.py",
]


description = "https://github.com/MichaelHaussmann/spil"

authors = ['Michael Haussmann']


def commands():
    env.PYTHONPATH.append('{root}')


is_pure_python = True
