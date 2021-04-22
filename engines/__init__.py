import sys
import six

if six.PY2:  # Path is imported by engines from here
    from pathlib2 import Path
else:
    from pathlib import Path


def get():
    """
    Get the current engine
    """
    if 'hou' in sys.executable:
        import engines.houdini_engine as he
        return he.HoudiniEngine()
    elif 'maya' in sys.executable:
        import engines.maya_engine as me
        return me.MayaEngine()
    elif 'Nuke' in sys.executable:
        import engines.nuke_engine as nuke
        return nuke.NukeEngine()
    else:  # default
        import engines.python_engine as py
        return py.PythonEngine()