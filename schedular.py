"""
This is all very rough but starting work on a time system for scheduling events.
"""

import time
import math 
import numpy as np
import audio
from play import Play

MINUTE = 60

class TimeKeeper():

    def __init__(self, stream):
        self._stream = stream
        self._time_0 = self._stream.get_time()

    def sample(self):
        now = self._stream.get_time()-self._time_0
        return now
    
    def schedule(self, from_past=.1):
        Play(self, from_past).start()

# it doesn't matter which stream we get, just get one to begin with since the
# audio device time is updated for any new stream we create
stream = audio.get_stream()
time_keeper = TimeKeeper(stream)

# sequential and asynch scheduling of audio play works 
# TODO fix issue of weird sounds when overlapping timelines
time_keeper.schedule(2.0)
time_keeper.schedule(1.5)
time_keeper.schedule(3.5)
time_keeper.schedule(3.0)

def bpm(num):
    return MINUTE / num
# print(bpm(120))