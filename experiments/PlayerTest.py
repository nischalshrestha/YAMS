from audio import sine, sawtooth, get_stream, w, normalize
from Player import Player

import numpy as np
import scipy as sc

from filters import *

import time

player = Player(continuous=False)
# wave = sine(440, lfo_amp=1.0, lfo_hz=5.0)
wave = sine(440) + sawtooth(220)
player.set_wave(wave.astype(np.float32))
# print(type(wave))
player.run()
# print(normalize(wave))

# cnt = 0
# def adsr(famp, duration, fr=44100):
#     global cnt
#     samples = []
#     a = 0.25 * fr
#     d = 0.25 * fr
#     s = .7 # amp
#     r = 0.75 * fr
#     amp = 0
#     if cnt < duration:
#         if cnt <= a:
#             amp = cnt * (famp / a)
#             # print('attack', famp)
#         elif cnt <= (a+d):
#             amp = ((s - famp)/d) * (cnt - a) + famp
#             # print('decay', famp)
#         elif cnt <= duration - r:
#             amp = s
#             # print('sustain', s)
#         elif cnt > duration - r:
#             amp = -(s/r) * (cnt - (duration - r)) + s
#             # print('release', famp)
#     else:
#         amp = 0.0
#     cnt += 1
#     return amp


# def osc(max_amp, freq, duration, fr=44100):
#     fr_duration = duration*fr
#     ts = np.arange(fr_duration) / fr
#     print(ts)
#     samples = []
#     for t in ts:
#         amp = adsr(max_amp, fr_duration, fr)
#         # print(amp)
#         # amp = max(0, min(1.0, amp))
#         phase = w(freq) * t
#         # phase = phase * sc.sin(w(0.5) * ts) # phase modulation
#         wave = amp * sc.sin(phase)
#     #     # print(wave)
#         samples.append(wave)
#     return np.array(samples)

# stream = get_stream()
# dur = 1.0
# wav = osc(1.0, 440, dur, 44100)
# print(wav)

# wav = sine()
# print(wav)
# stream.write(wav.astype(np.float32).tostring())

# wav = sine(440, duration=dur)
# sdur = dur * 44100

# a = np.linspace(0, 1, num=sdur*0.25)
# d = np.linspace(1, 0.8, num=sdur*0.25)
# s = np.repeat(0.8, repeats=sdur*0.25)
# r = np.linspace(0.8, 0, num=sdur*0.25)
# # r2 = np.linspace(0.3, 1, num=sdur*0.125)
# # rel = np.concatenate((r,r2))
# # print(rel.shape)
# envelope = np.concatenate((a, d, s, r))
# wav *= envelope
# stream.write(wav.tostring())


# time.sleep(5.0)
# player.stop()
