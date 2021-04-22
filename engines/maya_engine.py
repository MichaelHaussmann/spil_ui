import maya.cmds as cmds

from engines import Path
from spil import Sid, SpilException

from engines.python_engine import PythonEngine


class MayaEngine(PythonEngine):

    name = 'Maya'
    implements = ['explore','open']

    def open(self, sid):
        """
        Open file
        """
        # Set env variable / set Workspace
        try:
            path = Path(Sid(sid).path)
        except SpilException as e:
            print('Path for sid "{}" not found ({})'.format(sid, e))
            return

        if not path.exists():
            print('Path for sid "{}" does not exist ({})'.format(sid, path))
            return

        cmds.file(path, open=True, force=True)  # FIXME: force ?

    def save_next(self, sid, options={}):
        """

        """
        # get next
        # save comment
        # save file
        pass

    def get_current_sid(self):
        """
        Get the sid of the current file
        """
        path = cmds.file(query=True, sceneName=True)
        return Sid(path=path)

    def is_batch(self):
        return cmds.about(batch=True)


if __name__ == '__main__':

    sid = 'FTOT/A/CHR/COCO/MOD/V002/WIP/ma'
    print(Sid(sid).path)
    e = MayaEngine()
    print(e)
    # e.open(sid)
    e.open(sid)