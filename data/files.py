# -*- coding: utf-8 -*-
"""

    TO REFACTO - WIP - DRAFT - STUB




"""
try:
    from pathlib import Path
except:
    from pathlib2 import Path

import os
from logging import debug
from spil_ui.util.time_tools import toHumanReadableLapse

from spil import Sid


class Files(object):

    @staticmethod
    def getTime(sid, human=True):
        '''
        Returns the timestamp of the given sids file, or 0.
        If "human" is True, returns a human readable format (until second).
        '''
        path = Sid(sid).path
        if path:
            result = os.path.getmtime(path)
        else:
            result = 0
        if human:
            if result:
                result = toHumanReadableLapse(result)
            else:
                result = '--'

        return result

    @staticmethod
    def getComment(sid):
        """
        https://docs.python.org/3/library/pathlib.html#pathlib.Path.read_text
        """
        r = ''
        path = Path(Sid(sid).path).with_suffix('.comment')
        if path.exists():
            r = path.read_text() or ''
        return r

    @staticmethod
    def getSize(sid, human=True):

        path = Sid(sid).path
        size = 0
        try:
            size = os.path.getsize(path)
        except Exception as ex:
            debug(ex)

        if human:
            size = '{0:9.2f} Mo'.format((float(size) / (1024 * 1024)))

        return size


if __name__ == '__main__':

    p = r'V:\TESTPREMIERE\3_PROD\32_3D\322_SEQUENCES\SQ0001\SQ0001_SH0020\WIP\LAY\MAYA\EXPORT\SQ0001_SH0020_LAY_WIP_V005.mov'

    path = Path(p)
    print(path)
    print(path.stat())
    #print(path.owner())

    p = 'V:/FTRACK_ONLINE_TEST/3_PROD/32_3D/322_SEQUENCES/SQ0001/SQ0001_SH0020/WIP/LAY/MAYA/SQ0001_SH0020_LAY_WIP_V002.ma'
    sid = Sid(path=p)

    print(Files.getComment(sid))
