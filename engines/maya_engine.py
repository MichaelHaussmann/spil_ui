import maya.cmds as cmds

from spil import Sid, SpilException

from engines.python_engine import PythonEngine


class MayaEngine(PythonEngine):

    name = 'Maya'
    implements = ['explore','open']

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