import threading
from threading import Thread
import audio
from audio import generate_sine, generate_triangle, generate_sawtooth, generate_square
from audio import get_stream
from constants import *

class Metronome(threading.Thread):
    """
    Basic metronome given a timekeeper, the beats in bpm, type of note length 
    (quarter note etc.) and optionally a sound to play for the note
    """
    def __init__(self, time_keeper, beats, note_length, sound=None):
        Thread.__init__(self)
        self.stream = audio.get_stream()
        self.time_keeper = time_keeper
        self.beats = beats
        self.note_dur = note_length*beats
        self.silence = audio.silence(0.05)
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
                # print('beep', curr, 'pos', pos)
                self.stream.write(self.sound.tobytes())
                last = curr
    
    def set_sound(self, sound=None):
        self.sound = self.silence if sound is None else sound

    def stop(self):
        self.running = False