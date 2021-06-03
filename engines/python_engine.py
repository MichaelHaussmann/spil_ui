from spil import Sid
from engines.base_engine import BaseEngine


class PythonEngine(BaseEngine):  # FIXME: use rez to launch softwares

    name = 'Python'
    implements = ['explore']


if __name__ == '__main__':

    sid = 'FTOT/A/CHR/COCO/MOD/V002/WIP/ma'
    sid = 'FTOT/A/CHR/COCO/MOD'
    print(Sid(sid).path)
    e = PythonEngine()
    print(e)
    # e.open(sid)
    e.explore(sid)
