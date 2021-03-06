"""
This contains small sounds and tracks we can make with the system so far
"""

import numpy as np
import audio
import time
from audio import get_wave
from audio import triangle
from audio import write_wave
from audio import silence
from schedular import get_time_keeper
from effects import phase_off
from constants import *
from arpeggiator import Arpeggiator
from metropolis import Metropolis
from play import Play
from metronome import Metronome
from utility import beats_to_sec
import pyaudio as p

stream = audio.get_stream()

WAVE_OUTPUT_FILENAME = "testing.wav"
FR = 44100

def blast_off(play=False):
    # blast off to 440hz piece
    sample = np.array([])
    for i in range(1, 221):
        print('Hz:', i)
        sine = phase_off(freq=220, amount=i/2, off=i/2)
        sine2 = phase_off(freq=i, amount=i/3)
        if i >= 50:
            sine3 = triangle(i, duration=0.05, amp=i*.001, offset=i/3, taper=True) 
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

# blast_off(play=True)
sound = get_wave("triangle", 220, duration=0.1)
# stream.write(sound.tobytes())

mt = Metronome(get_time_keeper(), 120, SIXTEENTH, sound=sound)
mt.start()

def write_modes(file, play=False, iir="Rays.wav"):
    """Example of writing a series of notes to a file in some tempo"""
    print('Impulse:', iir)
    # 1/8 notes in 120bpm   
    dur = EIGHTH*bpm(120)
    silence = audio.silence(SIXTEENTH*dur) 
    samples = np.array([])
    for i, m in enumerate(MODES):
        mode_notes = audio.scale(440, m, 0.05, mode=True)
        for mn in mode_notes:
            samples = np.hstack((samples, mn, silence))
    convolved = audio.convolve_iir(samples, iir)
    if play:
        stream.write(convolved.tobytes())
    # you can simply stack the same samples by column if L/R are same
    target = np.stack((convolved, convolved), axis=1) # channels on separate axes
    write_wave(file, target)
    print('Successfully written to', file, ':)')

# Testing out different iir (source: http://www.voxengo.com/imodeler/)
# write_modes("test1.wav", play=True, iir="Nice Drum Room.wav")
# write_modes("test2.wav", play=True, iir="Rays.wav")
# write_modes("test3.wav", play=True, iir="Greek 7 Echo Hall.wav")
# write_modes("test4.wav", play=True, iir="Large Wide Echo Hall.wav")

# def pan_demo(duration, rotations=0):
#     left_sound = audio.normalize(audio.dominant(220, '7/6sus4', duration))
#     right_sound = np.copy(left_sound)
#     right = audio.apodize(np.linspace(0, duration, num=len(left_sound)))
#     left =  np.flip(right, axis=0)
#     lc = left_sound * left
#     rc = right_sound * right
#     left_chan = lc
#     right_chan = rc
#     for i in range(rotations):
#         left =  np.flip(left, axis=0)
#         right =  np.flip(right, axis=0)
#         new_left = left_sound * left
#         new_right = right_sound * right
#         left_chan = audio.normalize(np.hstack((left_chan, new_left)))
#         right_chan = audio.normalize(np.hstack((right_chan, new_right)))
#     target = np.stack((left_chan, right_chan), axis=1)  # channels on separate axes
#     write_wave(WAVE_OUTPUT_FILENAME, target)

# pan_demo(5, rotations=1)

# Experimenting with metropolis :D
# BPM = 120

# note_dur = beats_to_sec(EIGHTH, BPM)
# print("note duration", note_dur)
# sound = get_wave("triangle", 440, duration=0.05, taper=False)
# time_keeper = get_time_keeper()
# m = Metropolis(time_keeper, BPM, EIGHTH, 1, sound=sound, scale='aeolian')
# duration = 16*note_dur*1
# m.start()
# start = time_keeper.sample()
# print("start", start)
# print(f"BPM: {BPM} QUARTER")
# print("Pulse count 1")
# current = time_keeper.sample()
# while(current - start < duration):
#     current = time_keeper.sample()
# # m.stop()
# print("stop", current)
# print("accuracy", duration - (current-start))
# for i in range(2, 3):
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
# time.sleep(HALF*bpm(180)*6)
# arp2 = Arpeggiator(time_keeper, bpm(180), EIGHTH, 110, 'maj13', tone='maj', reverb=True)
# arp2.start()
# time.sleep(HALF*bpm(180)*4)
# arp3 = Arpeggiator(time_keeper, bpm(180), EIGHTH, 220, 'majadd9', tone='maj', reverb=True)
# arp3.start()
# time.sleep(HALF*bpm(180)*4)
# arp4 = Arpeggiator(time_keeper, 160, EIGHTH, 440, 'aeolian', scale=True, reverb=False, iir="Nice Drum Room.wav")
# arp4.start()
# time.sleep(WHOLE*bpm(180)*8)
# arp.stop()
# arp.join()
# arp2.stop()
# arp2.join()
# arp3.stop()
# arp3.join()
# arp4.stop()
# arp4.join()