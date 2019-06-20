"""
The sole purpose of this module is to play a sound on a thread at a given time
"""

import threading
import pyaudio
import audio
import time

class Play(threading.Thread):

    def __init__(self, time_keeper, when):
        threading.Thread.__init__(self)
        self._time_keeper = time_keeper
        self._when = when
        # TODO don't hardcode duration of signal
        self._wave = audio.generate_triangle(200, .5)
        self._p = pyaudio.PyAudio()

    def run(self):
        while self._time_keeper.sample() < self._when: continue
        s = self._p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                output=True)
        s.write(self._wave.tobytes())
        s.stop_stream()
        s.close()
        self._p.terminate()