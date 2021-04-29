# -*- coding: utf-8 -*-
"""
time_tools

Created on 1 fevr. 2012

Some timestamp converting tools.

Uses external lib : parsedatetime (Copyright 2009 Jai Vikram Singh Verma (jaivikram[dot]verma[at]gmail[dot]com), Apache Licence)

@author: michael haussmann

"""

from spil_ui.util.parsedatetime import convertToHumanReadable
import datetime
import time as to


def now():
    """ Returns the 'now' timestamp as an int """
    return int(to.time())


def toHumanReadableSecond(timestamp):
    return str(datetime.datetime.fromtimestamp(float( timestamp )).strftime('%Y-%m-%d %H:%M:%S'))

def toHumanReadableLapse(timestamp):
    return convertToHumanReadable(datetime.datetime.fromtimestamp(float( timestamp )).strftime('%Y-%m-%d %H:%M:%S.%f'))


'''

# Currently not used, not maintained



def toHumanReadableLapse(timestamp):
    return convertToHumanReadable(datetime.datetime.fromtimestamp(float( timestamp )).strftime('%Y-%m-%d %H:%M:%S.%f')) 

def toHumanReadableDay(timestamp):
    return str(datetime.datetime.fromtimestamp(float( timestamp )).strftime('%Y-%m-%d'))

def toHumanReadableDayHour(timestamp):
    return str(datetime.datetime.fromtimestamp(float( timestamp )).strftime('%Y%m%d-%H%M'))




def timecode_to_frames(timecode):
    framerate = int(Conf.framerate)
    return sum(f * int(t) for f,t in zip((3600*framerate, 60*framerate, framerate, 1), timecode.split(':')))

def frames_to_timecode(frames):
    framerate = int(Conf.framerate)
    return '{0:02d}:{1:02d}:{2:02d}:{3:02d}'.format(frames / (3600*framerate),
                                                    frames / (60*framerate) % 60,
                                                    frames / framerate % 60,
                                                    frames % framerate)
    
def tc_to_frame(hh, mm, ss, ff):
    frame_rate = int(Conf.framerate)
    return ff + (ss + mm*60 + hh*3600) * frame_rate

def frame_to_tc(fn):
    frame_rate = int(Conf.framerate)
    ff = fn % frame_rate
    s = fn // frame_rate
    return (s // 3600, s // 60 % 60, s % 60, ff)
'''