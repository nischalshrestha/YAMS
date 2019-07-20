import threading
from threading import Thread
from enum import Enum, auto
import numpy as np
from constants import *
import audio
from utility import beats_to_sec

class Modes(Enum):
    HOLD = auto()
    REPEAT = auto()
    SINGLE = auto()
    REST = auto()

# TODO UI to change parameters 
class Metropolis(threading.Thread):
    """
    Simplified version of intellijel's Metropolis module
    """
    def __init__(self, time_keeper, bpm, note_length, pulse_count, scale='ionian', sound=None):
        Thread.__init__(self)
        self.stream = audio.get_stream()
        self.time_keeper = time_keeper
        self.bpm = bpm
        self.note_length = note_length
        self.next_note = beats_to_sec(note_length, bpm)
        self.silence = audio.silence(self.next_note)
        self.pulse_count = pulse_count
        self.scale = MODES[scale]
        self.sound = self.silence if sound is None else sound 
        self.stages = [Stage(220, self.pulse_count, self.silence, Modes.REPEAT, 0.05) for i in range(len(self.scale))]
        # Currently just playing with setting some of the stages to HOLD
        # for s in range(len(self.stages)):
        #     if s % 5 == 0 or s % 7 == 0:
        #         self.stages[s].change_mode(Modes.HOLD)
        self.running = False
        self.samples = np.array([])
        self.count = 0 

    def set_main_note_length(self, note_length):
        self.note_length = note_length      
        self.next_note = beats_to_sec(note_length, self.bpm)
        self.silence = audio.silence(note_length)
    
    def set_main_pulse_count(self, pulse_count):
        self.pulse_count = pulse_count

    def run(self):
        self.running = True
        last = self.time_keeper.sample()
        pos = 0
        while self.running:
            curr = self.time_keeper.sample()
            if curr >= last + self.next_note:
                if pos >= len(self.stages): pos = 0
                stage = self.stages[pos]
                # print('Stage:', idx)
                new_pitch = 220 * (A) ** self.scale[np.random.randint(len(self.scale))]
                stage.change_sound(new_pitch, 0.05)
                # stage.change_pulse_count(np.random.randint(len(self.scale))+1)
                if stage.mode == Modes.HOLD:
                    # Hold the note for pulse count amount
                    stage.change_pulse_duration(stage.pulse_count*0.05)
                    self.stream.write(stage.sound.astype(np.float32).tobytes())
                    last = self.time_keeper.sample()
                elif stage.mode == Modes.REPEAT:
                    for p in range(stage.pulse_count):
                        self.stream.write(stage.sound.astype(np.float32).tobytes())
                        # self.stream.write(stage.pulse_silence.tobytes())
                        last = self.time_keeper.sample()
                pos += 1
    
    def set_sound(self, sound=None):
        self.sound = self.silence if sound is None else sound

    def stop(self):
        self.running = False

class Stage():
    """Represents each Stage of Metropolis"""
    # TODO add in slide, skip and ratchet later
    def __init__(self, pitch, pulse_count, pulse_silence, mode, duration):
        self.pitch = pitch
        self.sound = self.change_sound(pitch, 0.05)
        self.pulse_count = pulse_count
        self.pulse_silence = pulse_silence
        self.duration = duration
        self.mode = mode

    def change_sound(self, pitch, duration):
        self.pitch = pitch
        self.sound = audio.get_wave("triangle", pitch, duration) \
            + audio.get_wave("square", pitch/4, duration, amp=0.05) \
            + audio.get_wave("sawtooth", pitch/4, duration, amp=0.05) \
            + audio.get_wave("sine", pitch/2, duration)   
        return self.sound
        # print('new pitch', pitch)

    def change_pulse_count(self, pulse_count):
        self.pulse_count = pulse_count
        # print('new pulse count', pulse_count)
    
    def change_pulse_silence(self, pulse_silence):
        self.pulse_silence = audio.silence(pulse_silence)
        # print('new pulse length', pulse_silence)

    def change_pulse_duration(self, duration):
        self.duration = duration
        self.change_sound(self.pitch, duration)
        # print('new duration', duration)
    
    def change_mode(self, mode):
        self.mode = mode
        # print('new mode', mode)


    

