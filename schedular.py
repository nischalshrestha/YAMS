"""
This is all very rough but starting work on a time system for scheduling events.
"""

import time
import math 
import numpy as np
import audio

MINUTE = 60

class TimeKeeper():

    def __init__(self,):
        self._time_0 = time.time()
        self._last = time.time()

    def sample(self):
        now = time.time()-self._time_0
        return now

time_keeper = TimeKeeper()
curr = time_keeper.sample() 

def bpm(num):
    return MINUTE / num

# print(bpm(120))
cb = bpm(120)
duration = 4.0
last = curr

while curr <= duration + 0.5:
    curr = time_keeper.sample() 
    if round(curr, 1) % 2 == 0:
        audio.play()
        print(round(curr, 1))