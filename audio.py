#!/usr/bin/env python3
# ^ this is required for capturing key events
# you need to also give script executable right and run with sudo

"""
A playground for generating sounds for now but will be a audio playback or 
generation module
"""

import pyaudio
import numpy as np
from scipy import signal
from scipy.io import wavfile
import matplotlib.pyplot as plt

import time
import sys
from constants import *

# TODO add encapsulation with use of classes once different wave shapes
# can be generated
p = pyaudio.PyAudio()
fr = 44100
# fr = 10000
WAVE_OUTPUT_FILENAME = "output.wav"
CHANNELS = 1

# https://github.com/AllenDowney/ThinkDSP/blob/master/code/thinkdsp.py#L795
def apodize(ys, framerate=44100, denom=20, duration=0.1):
    """Tapers the amplitude at the beginning and end of the signal.
    Tapers either the given duration of time or the given
    fraction of the total duration, whichever is less.
    ys: wave array
    framerate: int frames per second
    denom: float fraction of the segment to taper
    duration: float duration of the taper in seconds
    returns: wave array
    """
    # a fixed fraction of the segment
    n = len(ys)
    k1 = n // denom
    # a fixed duration of time
    k2 = int(duration * framerate)
    k = min(k1, k2)
    w1 = np.linspace(0, 1, k)
    w2 = np.ones(n - 2*k)
    w3 = np.linspace(1, 0, k)
    window = np.concatenate((w1, w2, w3))
    return ys * window

# source: https://github.com/AllenDowney/ThinkDSP/blob/master/code/thinkdsp.py#L1068
def normalize(ys, amp=1.0):
    """Normalizes a wave array so the maximum amplitude is +amp or -amp.
    ys: wave array
    amp: max amplitude (pos or neg) in result
    returns: wave array
    """
    high, low = abs(max(ys)), abs(min(ys))
    return amp * ys / max(high, low)

# source: https://github.com/AllenDowney/ThinkDSP/blob/master/code/thinkdsp.py#L1058
def unbias(ys):
    """Shifts a wave array so it has mean 0.
    ys: wave array
    returns: wave array
    """
    return ys - ys.mean()

def generate_sine(freq=440, duration=1.0, start=0, offset=0, amp=1.0, taper=True):
    # makes sure that amp is within range [0.0, 1.0]
    amp = max(0, min(1.0, amp))
    # # framerate is the # samples per second so we divide each second by fr
    ts = start + np.arange(fr * duration) / fr
    # # This is the evaluation of the wave given the ts
    phases = 2 * np.pi * freq * ts  + offset
    # generate samples, note conversion to float32 array
    ys = amp * np.sin(phases)
    if taper: ys = apodize(ys)
    return ys.astype(np.float32)

def generate_triangle(freq=440, duration=1.0, start=0.0, offset=0, amp=1.0, taper=True):
    # makes sure that amp is within range [0.0, 1.0]
    amp = max(0, min(1.0, amp))
    ts = start + np.arange(fr * duration) / fr
    cycles = freq * ts + offset / 2*np.pi
    frac, _ = np.modf(cycles)
    ys = normalize(np.abs(frac - 0.5))
    ys = unbias(ys)
    silence = 0 * (np.arange(start * fr) / fr)
    ys = np.append(silence, ys)
    if taper: ys = apodize(ys)
    return ys.astype(np.float32)

def generate_square(freq=440, duration=1.0, start=0, offset=0, amp=1.0, taper=True):
    # makes sure that amp is within range [0.0, 1.0]
    amp = max(0, min(1.0, amp))
    ts = start + np.arange(fr * duration) / fr
    cycles = freq * ts + offset / 2*np.pi
    frac, _ = np.modf(cycles)
    ys = amp * np.sign(unbias(frac))
    if taper: ys = apodize(ys)
    return ys.astype(np.float32)

def generate_sawtooth(freq=440, duration=1.0, start=0, offset=0, amp=1.0, taper=True):
    ts = start + np.arange(fr * duration) / fr
    cycles = freq * ts + offset / 2*np.pi
    frac, _ = np.modf(cycles)
    ys = normalize(unbias(frac), amp)
    if taper: ys = apodize(ys)
    return ys.astype(np.float32)

def get_wave(wave_shape, freq, duration):
    if wave_shape == "triangle":
        wave = generate_triangle(freq=freq, duration=duration, taper=False)
    elif wave_shape == "sine":
        wave = generate_sine(freq=freq, duration=duration, taper=False)
    elif wave_shape == "square":
        wave = generate_square(freq=freq, duration=duration, amp=0.25, taper=False)
    elif wave_shape == "sawtooth":
        wave = generate_sawtooth(freq=freq, duration=duration, amp=0.25, taper=False)
    return wave

def callback(in_data, frame_count, time_info, status):
    end = callback.start_offset + frame_count
    data = callback.wave[callback.start_offset:end]
    callback.start_offset += frame_count
    # let pyaudio continue calling this function until there's no more data
    # to be read from wave
    return data, pyaudio.paContinue

callback.times = 0
callback.start_offset = 0

def major(root, formula, time):
    # equation for frequency calculation using equal-tempered scale: 
    # fn = f0 * (a)^n, fn = target freq, f0 is root, a = 2^(1/12)
    freqs = [root * (A) ** h for h in MAJOR_FORMULA[formula]]
    # generate the audio samples for each note and sum up for chord audio data
    # we need to normalize it to amp (for now just use default 1.0)
    return normalize(sum([generate_sawtooth(freq=f, duration=1.0) for f in freqs]))

def minor(root, formula, time):
    freqs = [root * (A) ** h for h in MINOR_FORMULA[formula]]
    return normalize(sum([generate_triangle(freq=f, duration=time) for f in freqs]))

def dominant(root, formula, time):
    freqs = [root * (A) ** h for h in DOMINANT_FORMULA[formula]]
    return normalize(sum([generate_triangle(freq=f, duration=time) for f in freqs]))

def write_wave(file_path, wave):
    wavfile.write(file_path, fr, wave)

def get_stream(callback=None):
    if callback is not None:
        return p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fr,
                    # input=True,
                    output=True,
                    stream_callback=callback)
    return p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fr,
                    # input=True,
                    output=True)

def clean_up():
    p.terminate()

def combine(a, b):
    c = np.zeros(max(len(a), len(b)))
    if len(a) < len(b):
        c = b.copy()
        c[:len(a)] += a
    else:
        c = a.copy()
        c[:len(b)] += b
    return c


# simple waves
sine_wave = generate_sine(freq=200)
callback.wave = sine_wave
# callback.wave = triangle_wave
# callback.wave = square_wave

# combinations

# triangle_wave = generate_triangle(freq=200)
# square_wave = generate_square(freq=40)
# callback.wave = sine_wave + square_wave
# callback.wave = sine_wave + triangle_wave
# callback.wave = triangle_wave + square_wave

# chords; testing lower pitch of A4 for now
# callback.wave = major(440/2, 'maj7/6')

# non-blocking
# stream = p.open(format=pyaudio.paFloat32,
#                 channels=1,
#                 rate=fr,
#                 # input=True,
#                 output=True,
#                 stream_callback=callback)
# start the stream
# from constants import *
# # wait for stream to finish because the audio playing is non-blocking
# while True:
#     # stream = get_stream(callback=callback)
#     # stream.start_stream()
#     time.sleep(0.1)
#     callback.start_offset = 0 
#     callback.times = 0
#     stream = get_stream(callback=callback)
#     stream.start_stream()

# blocking version
# the tobytes() is required due to pyaudio conversion of numpy	    
# https://stackoverflow.com/a/48454913/9193847
# for paFloat32 sample values must be in range [-1.0, 1.0]
# stream = p.open(format=pyaudio.paFloat32,
#                 channels=1,
#                 rate=fr,
# #                 # input=True,
#                 output=True)

# TODO experiment with simultaneous press?
# # playing with keyboard events; for now it makes it easy to debug sounds
# from pynput import keyboard

# def on_press(key):    
#     try:
#         print('alphanumeric key {0} pressed'.format(
#             key.char))
#         if key.char == 'q':
#             clean_up()
#             sys.exit(0)
#         elif (key.char.upper()+'0') in TABLE:
#             note = key.char.upper()+'3'
#             chord = major(TABLE[note], 'maj6', 0.2)
#             note = sine_table
#             stream.write(chord.tobytes())
#     except AttributeError:
#         pass
 
# def on_release(key):
#     print('Key {} released.'.format(key))
 
# with keyboard.Listener(
#     on_press = on_press,
#     on_release = on_release) as listener:
#     listener.join()


