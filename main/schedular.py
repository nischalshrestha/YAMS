"""
This is all very rough but starting work on a time system for scheduling events.
"""

import math 
import numpy as np
import threading
from threading import Thread
import pyaudio
import audio
from audio import sine, triangle, square
from audio import write_wave
from constants import *
from utility import beats_to_sec

fr = 44100

class TimeKeeper():

    def __init__(self, stream):
        self._stream = stream
        self._time_0 = self._stream.get_time()

    def sample(self):
        return self._stream.get_time()-self._time_0

# it doesn't matter which stream we get, just get one to begin with since the
# audio device time is updated for any new stream we create
# stream = audio.get_stream()
def get_time_keeper():
    return TimeKeeper(audio.get_stream())

class Metronome(threading.Thread):
    """
    Basic metronome given a timekeeper, the bpm, type of note length 
    (quarter note etc.) and optionally a sound to play for the note
    """
    def __init__(self, time_keeper, bpm, note_length, sound=None):
        Thread.__init__(self)
        self.stream = audio.get_stream()
        self.time_keeper = time_keeper
        self.note_dur = beats_to_sec(note_length, bpm)
        self.silence = audio.silence(self.note_dur)
        self.sound = self.silence if sound is None else sound
        self.running = False
    
    def run(self):
        self.running = True
        last = self.time_keeper.sample()
        while self.running:
            curr = self.time_keeper.sample()
            # instead of using exact time of play, calculate next time for more accuracy
            if curr >= last + self.note_dur:
                # since the write blocks for only the time it needs to, it will be
                # fairly accurate compared to time.sleep() which might drift
                # print('beep', curr)
                self.stream.write(self.sound)
                self.sound = self.silence
                last = curr
    
    def set_sound(self, sound=None):
        self.sound = self.silence if sound is None else sound

    def stop(self):
        self.running = False
        self.stream.close()

if __name__ == '__main__':
    sound = audio.get_wave("triangle", 440, duration=0.2)
    m = Metronome(get_time_keeper(), 120, QUARTER)
    m.set_sound(sound)
    m.start()
