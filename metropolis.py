import threading
from threading import Thread
from enum import Enum, auto
from constants import *
import audio
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
        self.note_dur = note_length*beats
        self.silence = audio.silence(note_length*beats)
        self.scale = MODES[scale]
        self.sound = self.silence if sound is None else sound 
        self.stages = [Stage(220, 1, Modes.SINGLE) for i in range(8)]
        self.running = False
        self.samples = []
    
    def set_stage_pulse(self, pos, pulse):
        self.stages[pos].pulse_count = pulse
        print('new pulse', pos, pulse)
    
    def set_stage_pitch(self, pos, pitch):
        self.stages[pos].change_pitch(pitch)
        print('new pitch', pos, pitch)        

    def run(self):
        self.running = True
        last = self.time_keeper.sample()
        pos = 0
        while self.running:
            curr = self.time_keeper.sample()
            if curr >= last + self.note_dur:
                idx = pos % len(self.stages)
                stage = self.stages[idx]
                self.set_stage_pitch(idx, 220 * (A) ** self.scale[np.random.randint(len(self.scale))])
                if idx == 2 or idx == 6:
                    self.set_stage_pulse(idx, np.random.randint(0, 8))
                if pos % len(self.stages) == 0:
                    print(stage)
                for p in range(stage.pulse_count):
                    self.stream.write(stage.pitch.tobytes())
                    self.stream.write(self.silence)
                    self.samples.extend(stage.pitch.tolist())
                    self.samples.extend(self.silence.tolist())
                    last = self.time_keeper.sample()
                pos += 1
    
    def set_sound(self, sound=None):
        self.sound = self.silence if sound is None else sound

    def stop(self):
        self.running = False

class Stage():
    """Represents each Stage of Metropolis"""
    # TODO add in slide, skip and ratchet later
    def __init__(self, pitch, pulse_count, mode):
        self.pitch = audio.get_wave("triangle", pitch, 0.05)
        self.pulse_count = pulse_count
        self.mode = mode

    def change_pitch(self, pitch):
        self.pitch = audio.get_wave("triangle", pitch, duration=0.05)  \
            + audio.get_wave("sine", pitch/2, 0.05)

    

