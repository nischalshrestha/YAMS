import threading
from threading import Thread
import audio
from audio import sine, triangle, sawtooth, square
from audio import get_stream
from constants import *
from utility import beats_to_sec

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
                last = curr
    
    def set_sound(self, sound=None):
        self.sound = self.silence if sound is None else sound

    def stop(self):
        self.running = False