import pyaudio
import numpy as np
import scipy as sc
from scipy import signal
from scipy.io import wavfile
from scipy.io.wavfile import read
from audio import *
from random import shuffle

wav = read("lightbath.wav")
fr = wav[0]
print(wav[1])
# just get the 30s of one channel
samples = wav[1].flatten()[fr*4:fr*20:2]
print(len(samples))
stream = get_stream(paformat=pyaudio.paInt16, num_channels=2, framerate=fr)

# Vibrato effect
grains = []
biggergrains = []
spacing = 3000 # higher the spacing, the glitchier the sound
grainsize = int((fr / 1000)*50)
for s in range(0, len(samples), grainsize):
    toadd = taper_wave(samples[s:s+grainsize]).tolist()
    grains.extend(toadd)
    for s in range(spacing):
        grains.append(0)

print('done', len(grains))
# print(grains)
w = taper_wave(np.array(grains))
target = np.stack((w, w), axis=1) # channels on separate axes
stream.write(target.astype(np.int16).tobytes())


