import nuke

from engines import Path
from spil import Sid, SpilException

from engines.python_engine import PythonEngine


class NukeEngine(PythonEngine):

    name = 'Nuke'
    implements = ['explore','open']

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

        nuke.scriptOpen(path)  # FIXME: force ?
        # self.set_env()
        # save: nuke.scriptSaveAs(path)

    def get_current_sid(self):
        """
        Get the sid of the current file
        """
        # return nuke.root().knob('name').value()  ?
        raise NotImplemented('TODO :)')

    def is_batch(self):
        return not nuke.GUI


if __name__ == '__main__':
    """
    Test
    """
    # Create engine
    engine = NukeEngine()
    print("Engine : " + str(engine))

