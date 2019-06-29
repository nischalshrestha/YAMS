"""
This contains small sounds and tracks we can make with the system so far
"""

import numpy as np
import audio
from audio import generate_triangle
from audio import write_wave
from audio import silence
from schedular import bpm
from effects import phase_off
from constants import *

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
    silence = audio.silence(EIGHTH*bpm(120)) 
    waves = []
    for i, m in enumerate(MODES):
        print(m)
        mode_notes = audio.mode(220, m, 0.05)
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

# TODO wrap this up in a method
# Example composition of arpeggios
# arp = Arpeggiator(time_keeper, bpm(180), EIGHTH, 55, 'maj', 'maj')
# arp.start()
# time.sleep(5)
# arp2 = Arpeggiator(time_keeper, bpm(180), EIGHTH, 110, 'maj', 'maj13')
# arp2.start()
# time.sleep(5)
# arp3 = Arpeggiator(time_keeper, bpm(180), EIGHTH, 220, 'maj', 'maj7')
# arp3.start()
# time.sleep(5)
# arp4 = Arpeggiator(time_keeper, bpm(60), EIGHTH, 440, 'maj', 'maj6/9')
# arp4.start()