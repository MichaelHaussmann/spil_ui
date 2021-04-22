
import hou

from engines import Path
from spil import Sid, SpilException

from engines.python_engine import PythonEngine


class HoudiniEngine(PythonEngine):

    name = 'Houdini'
    implements = ['explore', 'open']

    def open(self, sid):
        """
        Open file
        """
        #TODO : Set env variable / set Workspace
        try:
            path = Path(Sid(sid).path)
        except SpilException as e:
            print('Path for sid "{}" not found ({})'.format(sid, e))
            return

        if not path.exists():
            print('Path for sid "{}" does not exist ({})'.format(sid, path))
            return

        hou.hipFile.load(path, suppress_save_prompt=True)  # FIXME: force ?
        # self.set_env_var(path)

    def get_current_sid(self):
        """
        Get the sid of the current file
        """
        path = hou.hipFile.path()
        return Sid(path=path)

    def is_batch(self):
        return not hou.isUIAvailable()


if __name__ == '__main__':
    """
    Test
    """
    # Create engine
    engine = HoudiniEngine()
    print("Engine : " + str(engine))
