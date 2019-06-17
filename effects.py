"""
This will house all the functions that filter and trasform audio data 
"""

from audio import *

# TODO allowing UI to control parameters for each effect / filter

# weird alien ship pulse effect
# the end-start is how many modulations to do
# the amount is the wobbly-ness (TODO investigate the weird pulses at the ends of cycles)
# there is a relationship btw the number of modulations with the amount to modulate by
def phase_off(start=0, end=3, freq=440, off=0, amount=1, duration=0.05, amp=1.0):
    summation = generate_sine(freq, duration)
    for i in range(start, end):
        freq += amount
        summation += generate_sine(freq, duration, offset=off)
    return normalize(summation, amp)


# TODO arpeggiator



# TODO sequencer