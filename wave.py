import pyaudio
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

t = np.linspace(0, 1, 500)
plt.plot(t, signal.sawtooth(2 * np.pi * 5 * t))

import time

# TODO add encapsulation with use of classes once different wave shapes
# can be generated

p = pyaudio.PyAudio()
# fr = 44100
fr = 10000

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

def generate_sine(freq=440, duration=1.0, start=0, offset=0, amp=1.0):
    # makes sure that amp is within range [0.0, 1.0]
    amp = max(0, min(1.0, amp))
    # framerate is the # samples per second so we divide each second by fr
    ts = start + np.arange(fr * duration) / fr
    # This is the evaluation of the wave given the ts
    phases = 2 * np.pi * freq * ts  + offset
    # generate samples, note conversion to float32 array
    ys = amp * np.sin(phases).astype(np.float32)
    return ys

sine_wave = generate_sine(freq=200)
triangle_wave = generate_triangle(freq=200)

def callback(in_data, frame_count, time_info, status):
    end = callback.start_offset + frame_count
    data = callback.wave[callback.start_offset:end]
    callback.start_offset += frame_count
    # let pyaudio continue calling this function until there's no more data
    # to be read from wave
    return data, pyaudio.paContinue

callback.start_offset = 0
# callback.wave = sine_wave
callback.wave = triangle_wave

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fr,
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

p.terminate()