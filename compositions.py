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

# TODO make a 
WAVE_OUTPUT_FILENAME = "testing.wav"
def blast_off():
    # blast off to 440hz piece
    sample = []
    for i in range(1, 221):
        print('Hz:', i)
        sine = phase_off(freq=220, amount=i/2, off=i/2)
        sine2 = phase_off(freq=i, amount=i/3)
        if i >= 50:
            sine3 = generate_triangle(i, duration=0.05, amp=i*.001, offset=i/3)
            # we need to extend otherwise we would just have a 0 duration audio
            sample.extend((sine + sine2 + sine3).tolist())
            stream.write((sine + sine2 + sine3).tobytes())
        else:
            sample.extend((sine + sine2).tolist())
            stream.write((sine+sine2).tobytes())

    sine4 = phase_off(freq=440, end=3, amount=13, duration=0.5)
    stream.write(sine4.tobytes())
    sample.extend(sine4.tolist())
    write_wave(WAVE_OUTPUT_FILENAME, np.array(sample))
    print('Successfully written to', WAVE_OUTPUT_FILENAME, ':)')

def write_modes():
    """Example of writing a series of notes to a file in some tempo"""
    # 1/8 notes in 120bpm
    silence = audio.silence(SIXTEENTH*bpm(220)) 
    waves = []
    for i, m in enumerate(MODES):
        print(m)
        mode_notes = audio.scale(220, m, 0.05, mode=True)
        mn_list = [] 
        for mn in mode_notes:
            mn_list.extend(mn)
            mn_list.extend(silence)
            stream.write(mn.tobytes())
            stream.write(silence.tobytes())
        waves.extend(mn_list)
    write_wave(WAVE_OUTPUT_FILENAME, np.array(waves))
    print('Successfully written to', WAVE_OUTPUT_FILENAME, ':)')

# write_modes()

# Experimenting with metropolis :D
sound = get_wave("triangle", 220, duration=0.05)
m = Metropolis(get_time_keeper(), bpm(180), EIGHTH, sound=sound, scale='lydian')
m.start()

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