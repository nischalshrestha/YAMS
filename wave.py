import pyaudio
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import time
from constants import *

# TODO add encapsulation with use of classes once different wave shapes
# can be generated
p = pyaudio.PyAudio()
fr = 44100
# fr = 10000

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

def generate_triangle(freq=440, duration=1.0, start=0, offset=0, amp=1.0):
    # makes sure that amp is within range [0.0, 1.0]
    amp = max(0, min(1.0, amp))
    ts = start + np.arange(fr * duration) / fr
    cycles = freq * ts + offset / 2*np.pi
    frac, _ = np.modf(cycles)
    ys = np.abs(frac - 0.5)
    ys = normalize(unbias(ys), amp)
    return ys.astype(np.float32)

def generate_square(freq=440, duration=1.0, start=0, offset=0, amp=1.0):
    # makes sure that amp is within range [0.0, 1.0]
    amp = max(0, min(1.0, amp))
    ts = start + np.arange(fr * duration) / fr
    cycles = freq * ts + offset / 2*np.pi
    frac, _ = np.modf(cycles)
    ys = amp * np.sign(unbias(frac))
    return ys.astype(np.float32)

def generate_sine(freq=440, duration=1.0, start=0, offset=0, amp=1.0):
    # makes sure that amp is within range [0.0, 1.0]
    amp = max(0, min(1.0, amp))
    # framerate is the # samples per second so we divide each second by fr
    ts = start + np.arange(fr * duration) / fr
    # This is the evaluation of the wave given the ts
    phases = 2 * np.pi * freq * ts  + offset
    # generate samples, note conversion to float32 array
    ys = amp * np.sin(phases)
    return ys.astype(np.float32)

def callback(in_data, frame_count, time_info, status):
    end = callback.start_offset + frame_count
    data = callback.wave[callback.start_offset:end]
    callback.start_offset += frame_count
    # let pyaudio continue calling this function until there's no more data
    # to be read from wave
    return data, pyaudio.paContinue

callback.start_offset = 0

# TODO create functions to calculate some of this (steps, chords, scales etc.)
# equation for frequency calculation using equal-tempered scale: 
# fn = f0 * (a)^n, fn = target freq, f0 fixed note (440), a = 2^(1/12)
root = 440
# third would be 2 W up meaning 4 half steps
third = root * (A) ** 4
# third would be W, W, h, W up meaning 7 half steps
fifth = root * (A) ** 7
# generate the audio samples for each note
sine_wave_root = generate_sine(freq=root)
sine_wave_third = generate_sine(freq=third)
sine_wave_fifth = generate_sine(freq=fifth)
# set callback to the chords which is summation of the 3 notes
callback.wave = sine_wave_root + sine_wave_third + sine_wave_fifth

# callback.wave = sine_wave 
# callback.wave = triangle_wave
# callback.wave = square_wave

# combinations
# triangle_wave = generate_triangle(freq=200)
# square_wave = generate_square(freq=40)
# callback.wave = sine_wave + square_wave
# callback.wave = sine_wave + triangle_wave
# callback.wave = triangle_wave + square_wave

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fr,
                # input=True,
                output=True,
                stream_callback=callback)

# blocking version uses this and removes the stream_callback parameter in open()
# stream.write(sine_wave)
# stream.write(triangle_wave)

# non-blocking
# start the stream
stream.start_stream()
# wait for stream to finish because the audio playing is non-blocking
while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()
