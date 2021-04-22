import platform
import subprocess

from engines import Path
from spil import Sid, SpilException
from engines.base_engine import BaseEngine


class PythonEngine(BaseEngine):  #FIXME: use rez to launch softwares

    name = 'Python'
    implements = ['explore']

    def explore(self, sid):

        try:
            path = Path(Sid(sid).path)
        except SpilException as e:
            print('Path for sid "{}" not found ({})'.format(sid, e))
            return

        if not path.exists():
            print('Path for sid "{}" does not exist ({})'.format(sid, path))
            return

        if path.is_file():
            path = path.parent

        path = str(path)
        if platform.system() == "Windows":
            subprocess.Popen(["explorer", "/open,", path])
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def open(self, sid):
        """
        Open file
        """
        pass  # use rez



if __name__ == '__main__':

    sid = 'FTOT/A/CHR/COCO/MOD/V002/WIP/ma'
    sid = 'FTOT/A/CHR/COCO/MOD'
    print(Sid(sid).path)
    e = PythonEngine()
    print(e)
    # e.open(sid)
    e.explore(sid)
