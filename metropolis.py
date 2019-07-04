import threading
from threading import Thread
from enum import Enum, auto
from constants import *
import audio
from audio import write_wave
import numpy as np

class Modes(Enum):
    HOLD = auto()
    REPEAT = auto()
    SINGLE = auto()
    REST = auto()

class Metropolis(threading.Thread):
    """
    Simplified version of intellijel's Metropolis module
    """
    def __init__(self, time_keeper, beats, note_length, scale='ionian', sound=None):
        Thread.__init__(self)
        self.stream = audio.get_stream()
        self.time_keeper = time_keeper
        self.beats = beats
        self.note_length = note_length
        self.next_note = note_length*beats
        self.silence = audio.silence(note_length*beats)
        self.scale = MODES[scale]
        self.sound = self.silence if sound is None else sound 
        self.stages = [Stage(220, 1, self.silence, Modes.SINGLE) for i in range(8)]
        self.running = False
        self.samples = np.array([])
        self.count = 0
    
    def set_stage_pulse(self, pos, pulse):
        self.stages[pos].pulse_count = pulse
        print('new pulse', pos, pulse)
    
    def set_stage_pitch(self, pos, pitch):
        self.stages[pos].change_pitch(pitch)
        print('new pitch', pos, pitch)        

    def set_stage_pulse_length(self, pos, pulse_length):
        self.stages[pos].change_pulse_length(pulse_length)
        print('new pulse length', pos, pulse_length)

    def run(self):
        self.running = True
        last = self.time_keeper.sample()
        pos = 0
        while self.running:
            curr = self.time_keeper.sample()
            if curr >= last + self.next_note:
                idx = pos % len(self.stages)
                stage = self.stages[idx]
                print('Stage:', idx)
                self.set_stage_pitch(idx, 220 * (A) ** self.scale[np.random.randint(len(self.scale))])
                if idx == 0 or idx == 4:
                    self.set_stage_pulse(idx, np.random.randint(0, 8))
                for p in range(stage.pulse_count):
                    # TODO figure out why the samples is much slower than real time
                    # self.samples = np.hstack((self.samples, stage.pitch, stage.pulse_length))
                    self.stream.write(stage.pitch.tobytes())
                    self.stream.write(stage.pulse_length)
                    # self.count += len(stage.pitch) + len(stage.pulse_length)
                    last = self.time_keeper.sample()
                pos += 1
    
    def set_sound(self, sound=None):
        self.sound = self.silence if sound is None else sound

    def stop(self):
        self.running = False
        write_wave("metropolis.wav", self.samples)

class Stage():
    """Represents each Stage of Metropolis"""
    # TODO add in slide, skip and ratchet later
    def __init__(self, pitch, pulse_count, pulse_length, mode):
        self.pitch = audio.get_wave("triangle", pitch, 0.05)
        self.pulse_count = pulse_count
        # TODO come up with a better name for pulse_length bc it's rly silence
        self.pulse_length = pulse_length
        self.mode = mode

    def change_pitch(self, pitch):
        self.pitch = audio.get_wave("triangle", pitch, duration=0.05)  \
            + audio.get_wave("square", pitch/2, 0.05, amp=0.05)

    def change_pulse_length(self, pulse_length):
        self.pulse_length = audio.silence(pulse_length)
    

