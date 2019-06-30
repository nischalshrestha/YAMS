import threading
from threading import Thread
import audio
from audio import \
    generate_sine, generate_triangle, generate_sawtooth, generate_square
from audio import get_stream

class Oscillator(threading.Thread):
    """Basic oscillator that runs on its own thread"""

    def __init__(self, freq, wave_shape, duration=1.0):
        Thread.__init__(self)
        print(self.getName(), freq)
        self.stream = get_stream()
        self.wave = audio.get_wave(wave_shape, freq, duration, taper=False)
        self.running = False

    def generate(self):
        """A basic oscillator"""
        while True:
            yield self.wave
    
    def run(self):
        self.running = True
        while self.running:
            self.stream.write(self.wave.tobytes())
        self.stream.stop_stream()
        self.stream.close()

    def stop(self):
        self.running = False