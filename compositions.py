"""
This contains small sounds and tracks we can make with the system so far
"""

import numpy as np
import audio
import time
from audio import get_wave
from audio import generate_triangle
from audio import write_wave
from audio import silence
from schedular import bpm, get_time_keeper
from effects import phase_off
from constants import *
from arpeggiator import Arpeggiator
from metropolis import Metropolis

stream = audio.get_stream()

WAVE_OUTPUT_FILENAME = "testing.wav"

def blast_off(play=False):
    # blast off to 440hz piece
    sample = np.array([])
    for i in range(1, 221):
        print('Hz:', i)
        sine = phase_off(freq=220, amount=i/2, off=i/2)
        sine2 = phase_off(freq=i, amount=i/3)
        if i >= 50:
            sine3 = generate_triangle(i, duration=0.05, amp=i*.001, offset=i/3) 
            next_sound = sine + sine2 + sine3
            sample = np.hstack((sample, next_sound))
            if play:
                stream.write(next_sound.tobytes())
        else:
            next_sound = sine + sine2
            sample = np.hstack((sample, next_sound))
            if play:
                stream.write(next_sound.tobytes())
    next_sound = phase_off(freq=440, end=3, amount=13, duration=0.5)
    if play:
        stream.write(next_sound.tobytes())
    sample = np.hstack((sample, next_sound))
    write_wave(WAVE_OUTPUT_FILENAME, sample)
    print('Successfully written to', WAVE_OUTPUT_FILENAME, ':)')

# blast_off()

def write_modes(play=False):
    """Example of writing a series of notes to a file in some tempo"""
    # 1/8 notes in 120bpm
    silence = audio.silence(SIXTEENTH*bpm(220)) 
    samples = np.array([])
    for i, m in enumerate(MODES):
        print(m)
        mode_notes = audio.scale(220, m, 0.05, mode=True)
        for mn in mode_notes:
            if play:
                stream.write(mn.tobytes())
                stream.write(silence.tobytes())
            samples = np.hstack((samples, mn, silence))
    # you can simply stack the same samples by column if L/R are same
    target = np.stack((samples, samples), axis=1)  # channels on separate axes
    write_wave(WAVE_OUTPUT_FILENAME, target)
    print('Successfully written to', WAVE_OUTPUT_FILENAME, ':)')


def pan_demo(duration, rotations=0):
    left_sound = audio.normalize(audio.dominant(220, '7/6sus4', duration))
    right_sound = np.copy(left_sound)
    right = audio.apodize(np.linspace(0, duration, num=len(left_sound)))
    left =  np.flip(right, axis=0)
    lc = left_sound * left
    rc = right_sound * right
    left_chan = lc
    right_chan = rc
    for i in range(rotations):
        left =  np.flip(left, axis=0)
        right =  np.flip(right, axis=0)
        new_left = left_sound * left
        new_right = right_sound * right
        left_chan = audio.normalize(np.hstack((left_chan, new_left)))
        right_chan = audio.normalize(np.hstack((right_chan, new_right)))
    target = np.stack((left_chan, right_chan), axis=1)  # channels on separate axes
    write_wave(WAVE_OUTPUT_FILENAME, target)

# pan_demo(5, rotations=1)

# write_modes(True)

# Experimenting with metropolis :D
# sound = get_wave("triangle", 120, duration=0.05)
# time_keeper = get_time_keeper()
# m = Metropolis(time_keeper, bpm(220), QUARTER, 1, sound=sound, scale='dorian')
# duration = 8*EIGHTH*bpm(180)*3
# m.start()
# print("BPM: 220 QUARTER")
# print("Pulse count 1")
# time.sleep(duration)
# for i in range(2, 6):
#     print(f'Pulse count {i}')
#     m.set_main_pulse_count(i)
#     time.sleep(duration)
# print("BPM: 220 EIGHTH")
# m.set_main_note_length(EIGHTH)
# for i in range(1, 6):
#     print(f'Pulse count {i}')
#     m.set_main_pulse_count(i)
#     time.sleep(duration)
# print("BPM: 220 SIXTEENTH")
# m.set_main_note_length(SIXTEENTH)
# for i in range(1, 6):
#     print(f'Pulse count {i}')
#     m.set_main_pulse_count(i)
#     time.sleep(duration)
# print("BPM: 220 THIRTY-SECOND") 
# m.set_main_note_length(THIRTY_SECOND)
# for i in range(1, 6):
#     print(f'Pulse count {i}')
#     m.set_main_pulse_count(i)
#     time.sleep(duration)
# print("BPM: 220 SIXTY-SECOND") 
# m.set_main_note_length(SIXTY_FOURTH)
# for i in range(1, 6):
#     print(f'Pulse count {i}')
#     m.set_main_pulse_count(i)
#     time.sleep(duration)
# m.stop()

# TODO wrap this up in a method
# Example composition of arpeggios
# time_keeper = get_time_keeper()
# arp = Arpeggiator(time_keeper, bpm(180), EIGHTH, 55, 'maj', tone='maj')
# arp.start()
# time.sleep(5)
# arp2 = Arpeggiator(time_keeper, bpm(180), EIGHTH, 110, 'maj13', tone='maj')
# arp2.start()
# time.sleep(5)
# arp3 = Arpeggiator(time_keeper, bpm(180), EIGHTH, 220, 'majadd9', tone='maj')
# arp3.start()
# time.sleep(5)
# arp4 = Arpeggiator(time_keeper, bpm(60), EIGHTH, 440, 'maj6/9', tone='maj')
# arp4.start()