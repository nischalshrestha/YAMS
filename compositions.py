"""
This contains small sounds and tracks we can make with the system so far
"""

import audio
from audio import generate_triangle
from audio import write_wave
from effects import phase_off

stream = audio.get_stream()

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
print('Successfully written to', WAVE_OUTPUT_FILENAME+'! :)')