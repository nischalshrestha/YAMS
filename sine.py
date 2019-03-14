import pyaudio
import numpy as np

# Note: this blocks

p = pyaudio.PyAudio()

amp = 0.5     # range [0.0, 1.0]
fr = 44100       # sampling rate, Hz, must be integer
duration = 1.0   # in seconds, may be float
f = 440.0        # sine frequency, Hz, may be float

start = 0
offset = 0

# framerate is the # samples per second so we divide each second by fr
ts = start + np.arange(fr * duration)
# This is the evaluation of the wave given the ts
phases = 2 * np.pi * f * ts  + offset
# generate samples, note conversion to float32 array
ys = (amp * np.sin(phases)).astype(np.float32).tobytes()

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fr,
                output=True)

# play. May repeat with different volume values (if done interactively) 
stream.write(ys)

stream.stop_stream()
stream.close()

p.terminate()