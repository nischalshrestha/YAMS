import threading
from threading import Thread
from constants import *
import audio
import numpy as np
from play import Play
from pyaudio import paFloat32

# TODO Make a Base class Sequencer that will allow us to create many different
# kinds of sequencers; perhaps Metronome is more of a base class

# TODO add a write mode for writing the waves directly to wave file

class Arpeggiator(threading.Thread):
    """
    Basic sequencer
    """
    def __init__(self, time_keeper, beats, note_length, root, formula, \
                tone='maj', scale=False, reverb=False, iir="Small Drum Room.wav"):
        Thread.__init__(self)
        self.stream = audio.get_stream(paformat=paFloat32)
        self.time_keeper = time_keeper
        self.note_dur = note_length*beats
        self.silence = audio.silence(self.note_dur)
        self.reverb = reverb
        self.iir = iir
        # TODO make this more robust
        if not scale:
            if tone == 'maj':
                self.steps = audio.major(root, formula, 0.05, arp=True)
            elif tone == 'min':
                self.steps = audio.minor(root, formula, 0.05, arp=True)
            elif tone == 'dom':
                self.steps = audio.dominant(root, formula, 0.05, arp=True)
        else:
            self.steps = audio.scale(root, formula, 0.05, mode=True)
        self.running = False
    
    def run(self):
        self.running = True
        last = self.time_keeper.sample()
        pos = 0
        while self.running:
            curr = self.time_keeper.sample()
            if curr >= last + self.note_dur:
                if pos >= len(self.steps): pos = 0
                data = audio.convolve_iir(self.steps[pos], self.iir)
                if self.reverb:
                    playit = Play(data)
                    playit.start()
                    # self.stream.write(self.steps[pos])
                else:
                    self.stream.write(self.steps[pos].tobytes())
                last = curr
                pos += 1
    
    def set_sound(self, sound=None):
        self.sound = self.silence if sound is None else sound

    def stop(self):
        self.running = False
        self.join()