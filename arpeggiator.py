import time
import threading
from threading import Thread
# import schedular
# from schedular import TimeKeeper
from constants import *
import audio
import numpy as np

# TODO Make a Base class Sequencer that will allow us to create many different
# kinds of sequencers; perhaps Metronome is more of a base class

# TODO add a write mode for writing the waves directly to wave file

class Arpeggiator(threading.Thread):
    """
    Basic sequencer
    """
    def __init__(self, time_keeper, beats, note_length, root, formula, tone='maj', scale=False):
        Thread.__init__(self)
        self.stream = audio.get_stream()
        self.time_keeper = time_keeper
        self.beats = beats
        self.note_dur = note_length*beats
        # TODO make this more robust
        if not scale:
            if tone == 'maj':
                self.steps = audio.major(root, formula, 0.05, arp=True)
            elif tone == 'min':
                self.steps = audio.minor(root, formula, 0.05, arp=True)
            elif tone == 'dom':
                self.steps = audio.dominant(root, formula, 0.05, arp=True)
        else:
            self.steps = audio.mode(root, formula, 0.05)
        self.running = False
    
    def run(self):
        self.running = True
        last = self.time_keeper.sample()
        pos = 0
        while self.running:
            curr = self.time_keeper.sample()
            if curr >= last + self.note_dur:
                self.stream.write(self.steps[pos].tobytes())
                last = curr
                pos = pos + 1 if (pos + 1) < len(self.steps) else 0
    
    def set_sound(self, sound=None):
        self.sound = self.silence if sound is None else sound

    def stop(self):
        self.running = False