import pyaudio
import numpy as np
import time

# Note: this blocks main thread

p = pyaudio.PyAudio()

fr = 44100       # sampling rate, Hz, must be integer

def generate_wave(freq=440, duration=1.0, start=0, offset=0, amp=1.0):
    # makes sure that amp is within range [0.0, 1.0]
    amp = max(0, min(1.0, amp))
    # framerate is the # samples per second so we divide each second by fr
    ts = start + np.arange(fr * duration) / fr
    # This is the evaluation of the wave given the ts
    phases = 2 * np.pi * freq * ts  + offset
    # generate samples, note conversion to float32 array
    # the tobytes() is required due to pyaudio conversion of numpy
    # https://stackoverflow.com/a/48454913/9193847
    ys = (amp * np.sin(phases).astype(np.float32))
    return ys.tobytes()

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fr,
                output=True)

# play. May repeat with different volume values (if done interactively) 
stream.write(generate_wave(freq=440, amp=0.9))

stream.stop_stream()
stream.close()

p.terminate()