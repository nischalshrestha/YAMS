"""
This is all very rough but starting work on a time system for scheduling events.
"""

import time
import math 
import numpy as np
import audio
from audio import generate_triangle
from audio import generate_square
from audio import generate_sine
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
stream = audio.get_stream()
time_keeper = TimeKeeper(stream)

def bpm(num):
    return MINUTE / num

# TODO can add frequency type as well
def metronome(note, beats, wave_type):
    """
    Basic metronome given type of note length (quarter note etc.) the beats
    in bpm and wave type
    """
    base_dur = beats
    note_dur = note*base_dur
    if wave_type == "triangle":
        wave = generate_triangle(freq=220, duration=0.05)
    elif wave_type == "sine":
        wave = generate_sine(freq=220, duration=0.05)
    elif wave_type == "square":
        wave = generate_square(freq=220, duration=0.05, amp=0.5)
    last = time_keeper.sample()
    while True:
        curr = time_keeper.sample()
        # instead of using exact time of play, calculate next time for more accuracy
        if curr >= last + note_dur:
            # since the write blocks for only the time it needs to, it will be
            # fairly accurate compared to time.sleep() which might drift
            stream.write(wave.tobytes())
            last = curr

metronome(EIGHTH, bpm(120), "triangle")

# TODO can add frequency type as well
def play_notes_for(note, duration, beats):
    """Plays a note length for duration given beats in bpm"""
    base_dur = QUARTER*beats
    note_dur = note*base_dur
    times = np.arange(1, duration, note_dur)
    wave = generate_triangle(freq=220, duration=0.05)
    last = time_keeper.sample()
    while last < duration:
        curr = time_keeper.sample()
        if curr >= last + note_dur:
            stream.write(wave.tobytes())
            last = curr

# play_notes_for(QUARTER, 5, bpm(120))
