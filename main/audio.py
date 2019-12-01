"""
A playground for generating sounds for now but will be a audio playback or 
generation module
"""

import pyaudio
import numpy as np
import scipy as sc
from scipy import signal
from scipy.io import wavfile
from scipy.io.wavfile import read
from scipy.signal import fftconvolve 
import threading

import time
import sys
from constants import *

# TODO add encapsulation with use of classes once different wave shapes
# can be generated
FR = 44100
# fr = 10000
WAVE_OUTPUT_FILENAME = "output.wav"
CHANNELS = 1
TWOPI = 2*np.pi
p = pyaudio.PyAudio()

# source: https://github.com/AllenDowney/ThinkDSP/blob/master/code/thinkdsp.py#L1068
def normalize(ys, amp=1.0):
    """Normalizes a wave array so the maximum amplitude is +amp or -amp.
    ys: wave array
    amp: max amplitude (pos or neg) in result
    returns: wave array
    """
    high, low = abs(max(ys)), abs(min(ys))
    return amp * ys / max(high, low)

def unbias(ys):
    """Shifts a wave array so it has mean 0.
    ys: wave array
    returns: wave array
    """
    return ys - ys.mean()

def w(freq):
    """Returns angular frequency"""
    return freq * TWOPI

def taper_wave(wave, fr=FR, factor=20, duration=.1):
    """
    Tapers the beginning and end of a wave to avoid clicks from steep
    increase/decrease in amplitude based on fraction of the wave or duration.
    """
    wave_len = len(wave)
    taper = min(wave_len // factor, int(fr * duration))
    beg = np.linspace(0, 1, taper)
    mid = np.ones(wave_len - 2*taper)
    end = np.linspace(1, 0, taper)
    amp = np.concatenate((beg, mid, end))
    return amp * wave

def sine(freq=440, amp=1.0, duration=1.0, offset=0, taper=False, \
        lfo_hz=0.0, lfo_amp=0.0, amp_lfo=0.0, waveFormat=np.float32):
    """Returns a sine wave, tapering if needed"""
    amp = max(0, min(1.0, amp))
    ts = np.arange(FR * duration) / FR 
    phase = w(freq) * ts + lfo_amp * sc.sin(w(lfo_hz) * ts)
    amps = normalize(amp + sc.sin(w(amp_lfo) * ts), amp)
    # phase = phase * sc.sin(w(0.5) * ts) # phase modulation
    wave = amps * sc.sin(phase)
    return taper_wave(wave, FR).astype(waveFormat) if taper else wave.astype(waveFormat)

def square(freq=440, amp=1.0, duration=1.0, offset=0, taper=False, \
        lfo_hz=0.0, lfo_amp=0.0, amp_lfo=0.0, waveFormat=np.float32):
    """Returns a sine wave, tapering if needed"""
    amp = max(0, min(1.0, amp)) / 6  # square is harsh so let's reduce amp
    ts = np.arange(FR * duration) / FR 
    phase = w(freq) * ts + lfo_amp * sc.sin(w(lfo_hz) * ts)
    amps = normalize(amp + sc.sin(w(amp_lfo) * ts), amp)
    s = amps * sc.sin(phase)
    wave = amps * np.sign(s)
    return taper_wave(wave, FR).astype(waveFormat) if taper else wave.astype(waveFormat)

def triangle(freq=440, amp=1.0, duration=1.0, offset=0, taper=False, \
            lfo_hz=0.0, lfo_amp=0.0, amp_lfo=0.0, waveFormat=np.float32):
    """Returns a sine wave, tapering if needed"""
    amp = max(0, min(1.0, amp))
    ts = np.arange(FR * duration) / FR 
    phase = w(freq) * ts + lfo_amp * sc.sin(w(lfo_hz) * ts)
    amps = normalize(amp + sc.sin(w(amp_lfo) * ts), amp)
    s = amps * sc.sin(phase)
    wave = (2 / np.pi) * sc.arcsin(s)
    return taper_wave(wave, FR).astype(waveFormat) if taper else wave.astype(waveFormat)

def sawtooth(freq=440, amp=1.0, duration=1.0, offset=0, taper=False, \
            lfo_hz=0.0, lfo_amp=0.0, amp_lfo=0.0, analog=False, waveFormat=np.float32):
    """Returns a sawtooth wave, tapering if needed"""
    amp = max(0, min(1.0, amp)) / 6
    ts = np.arange(FR * duration) / FR 
    phase = w(freq) * ts + lfo_amp * sc.sin(w(lfo_hz) * ts)
    amps = amp + sc.sin(w(amp_lfo) * ts)
    if analog:
         # analog way (sounds warmer but is slower to compute)
        waves = []
        for n in range(1, 51):
            waves.append((sc.sin(phase * n)) / n)
        wave = normalize(amps*sum(waves), amp)
    else:
        # modf way (doesn't sound as nice but faster to compute)
        frac, _ = amps * np.modf(phase / TWOPI)
        wave = frac - 1
    return taper_wave(wave, FR).astype(waveFormat) if taper else wave.astype(waveFormat)

def ucnoise(duration, amp=1.0, waveFormat=np.float32):
    """Uncorrelated noise"""
    ts = np.arange(FR * duration) / FR 
    wave = normalize(np.random.uniform(-amp, amp, len(ts)), amp)
    return taper_wave(wave,FR).astype(waveFormat)

def bnoise(duration, amp=1.0, waveFormat=np.float32):
    """Brownian noise"""
    ts = np.arange(FR * duration) / FR 
    dys = np.random.uniform(-1, 1, len(ts))
    wave = normalize(np.cumsum(dys) - 1, amp)
    return taper_wave(wave,FR).astype(waveFormat)

def wnoise(duration, amp=1.0, waveFormat=np.float32):
    """White noise"""
    ts = np.arange(FR * duration) / FR 
    wave = normalize(np.random.normal(0, amp, len(ts)), amp)
    return taper_wave(wave, FR).astype(waveFormat)

def get_wave(wave_shape, freq, duration, amp=1.0, taper=True):
    if wave_shape == "triangle":
        wave = triangle(freq=freq, duration=duration, amp=amp, taper=taper)
    elif wave_shape == "sine":
        wave = sine(freq=freq, duration=duration, amp=amp, taper=taper)
    elif wave_shape == "square":
        wave = square(freq=freq, duration=duration, amp=amp, taper=taper)
    elif wave_shape == "sawtooth":
        wave = sawtooth(freq=freq, duration=duration, amp=amp, taper=taper)
    return wave

def silence(duration):
    return get_wave("triangle", 0, duration)

def scale(root, formula, time, mode=False):
    scales = MODES if mode else SCALES
    freqs = [root * (A) ** h for h in scales[formula]]
    # TODO create a function to compose waves more easily
    # testing composition of waves for each note in scale
    return [triangle(freq=f, duration=time, lfo_amp=1.0, lfo_hz=5.0, taper=True) \
        + sawtooth(freq=f, duration=time, amp=1.0, lfo_amp=1.0, lfo_hz=5.0, taper=True) for f in freqs]

def major(root, formula, time, arp=False):
    # equation for frequency calculation using equal-tempered scale: 
    # fn = f0 * (a)^n, fn = target freq, f0 is root, a = 2^(1/12)
    freqs = [root * (A) ** h for h in MAJOR_FORMULA[formula]]
    # generate the audio samples for each note and sum up for chord audio data
    # we need to normalize it to amp (for now just use default 1.0)
    if arp:
        return [triangle(freq=f, duration=time, taper=True, lfo_amp=1.0, lfo_hz=5.0) for f in freqs]
    return normalize(sum([triangle(freq=f, duration=time) for f in freqs]))

def minor(root, formula, time, arp=False):
    freqs = [root * (A) ** h for h in MINOR_FORMULA[formula]]
    if arp:
        return [triangle(freq=f, duration=time) for f in freqs]
    return normalize(sum([triangle(freq=f, duration=time) for f in freqs]))

def dominant(root, formula, time, arp=False, taper=False):
    freqs = [root * (A) ** h for h in DOMINANT_FORMULA[formula]]
    if arp:
        return [triangle(freq=f, duration=time, taper=taper) for f in freqs]
    return normalize(sum([triangle(freq=f, duration=time, taper=taper) for f in freqs]))

def convolve_iir(data, iir):
    a = read("../IMreverbs/"+iir)
    impulse_response = np.array(a[1], dtype=float)[:, 0]
    convolved = normalize(fftconvolve(data, impulse_response)).astype(np.float32)
    return convolved

def write_wave(file_path, wave):
    wavfile.write(file_path, FR, wave)

def get_stream(callback=None, paformat=pyaudio.paFloat32, num_channels=1, chan_map=(), framerate=44100, frame_size=1024):
    if callback is not None:
        return p.open(format=paformat,
                    channels=num_channels,
                    rate=framerate,
                    # input=True,
                    frames_per_buffer=frame_size,
                    output=True,
                    stream_callback=callback)
    return p.open(format=paformat,
                    channels=num_channels,
                    rate=framerate,
                    frames_per_buffer=frame_size,
                    # input=True,
                    output=True)

def clean_up():
    p.terminate()

# stream = get_stream(frame_size=1024)
# duration = 1.0
# table = sine(duration=duration)
# # stream.write(table.tobytes())

# index = 0
# vecsize = 64
# output = np.zeros(vecsize)

# def oscil(amp, freq, length=vecsize, fr=44100):
#     global output, table, index 
#     incr = freq*length/fr
#     for i in range(vecsize):
#         # truncated lookup
#         # print(table[int(index)])
#         output[i] = amp * table[int(index)]
#         index += incr
#         while index >= length: index -= length
#         while index < 0: index += length
#     return output

# dur = int(duration*44100/vecsize) # duration in control samples
# for i in range(dur):
#     stream.write(oscil(0.5, 440).astype(np.float32).tostring())
# print(len(output))


# simple waves
# sine_wave = sine(freq=200)
# callback.wave = sine_wave
# callback.wave = triangle_wave
# callback.wave = square_wave

# combinations

# triangle_wave = triangle(freq=200)
# square_wave = square(freq=40)
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

