"""
This will house all the functions that filter and trasform audio data 
"""

from audio import sine, normalize

def delay(w, d=3.0):
    """simple echo delay"""
    N = len(w)
    amount = d*FR
    echo = np.zeros(int(N + amount))
    for s in range(0, len(echo)):
        echo[s] = w[s] if s < N else 0
        echo[s] += (0.5*w[int(s-amount)] if s >= amount else 0)
    return echo

# TODO allowing UI to control parameters for each effect / filter

# weird alien ship pulse effect
# the end-start is how many modulations to do
# the amount is the wobbly-ness (TODO investigate the weird pulses at the ends of cycles)
# there is a relationship btw the number of modulations with the amount to modulate by
def phase_off(start=0, end=3, freq=440, off=0, amount=1, duration=0.05, amp=1.0):
    summation = sine(freq, duration=duration, taper=True)
    for i in range(start, end):
        freq += amount
        summation += sine(freq=freq, duration=duration, offset=off, taper=True)
    return normalize(summation, amp)