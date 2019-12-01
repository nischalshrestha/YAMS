"""
The sole purpose of this module is to play a sound on a thread at a given time
"""

import threading
import pyaudio
import audio
import time
import numpy as np

FR = 44100

class Play(threading.Thread):

    def __init__(self, wave):
        threading.Thread.__init__(self)
        self.stream = audio.get_stream()
        self.wave = wave
        self.release = False

    def run(self):
        # sort of using a "table lookup"
        # t = 0
        # while not self.release:
        #     self.stream.write(self.wave[t % len(self.wave)].astype(np.float32).tobytes())
        #     t += 1
        self.stream.write(self.wave.astype(np.float32).tobytes())
        self.stream.stop_stream()
        self.stream.close()
    
    def stop(self):
        self.release = True
