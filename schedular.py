"""
This is all very rough but starting work on a time system for scheduling events.
"""

import time
import math 
import numpy as np
import audio
import pyaudio
from audio import generate_triangle
from audio import generate_square
from audio import generate_sine
from audio import write_wave
from oscillator import Oscillator
from metronome import Metronome
from arpeggiator import Arpeggiator
from constants import *

# TODO clean up when program is quit unexpectedly (ctrl c or other)

fr = 44100

class TimeKeeper():

    def __init__(self, stream):
        self._stream = stream
        self._time_0 = self._stream.get_time()

    def sample(self):
        now = self._stream.get_time()-self._time_0
        return now

# it doesn't matter which stream we get, just get one to begin with since the
# audio device time is updated for any new stream we create
# stream = audio.get_stream()
def get_time_keeper():
    return TimeKeeper(audio.get_stream())

def bpm(num):
    return MINUTE / num

# sound = audio.get_wave("triangle", 220, duration=0.05)
# m = Metronome(get_time_keeper(), bpm(120), EIGHTH)
# m.set_sound(sound)
# m.start()

# osc = Oscillator(220, "triangle")
# osc.start()
# osc.stop()

# TODO add wave shape
def play_notes_for(freq, note, duration, beats):
    """Plays a note length for duration given beats in bpm"""
    base_dur = QUARTER*beats
    note_dur = note*base_dur
    times = np.arange(1, duration, note_dur)
    wave = generate_triangle(freq=freq, duration=0.05)
    last = time_keeper.sample()
    while last < duration:
        curr = time_keeper.sample()
        if curr >= last + note_dur:
            stream.write(wave.tobytes())
            last = curr

# play_notes_for(220, QUARTER, 5, bpm(120))
