"""
The sole purpose of this module is to play a sound on a thread at a given time
"""

import threading
import pyaudio
import audio
import time

class Play(threading.Thread):

    def __init__(self, wave, silence=None):
        threading.Thread.__init__(self)
        # TODO don't hardcode duration of signal
        self.wave = wave
        self.silence = silence

    def run(self):
        s = audio.get_stream()
        s.write(self.wave.tobytes())
        s.write(self.silence.tobytes())
        s.stop_stream()
        s.close()
