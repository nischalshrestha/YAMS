"""
This contains useful functions
"""

from constants import *
from numpy.fft import fft
from numpy.fft import fftfreq
from numpy.fft import ifft

def high_pass(ys, cutoff, factor=0, framerate=44100):
    """
    Attenuate frequencies below the cutoff.

    ys -- the wave (numpy array)
    cutoff -- frequency (Hz)
    factor -- what to multiply the magnitude by
    framerate -- framerate of wave
    """
    n = len(ys)
    d = 1 / framerate
    # need to fft to compute amplitudes for frequencies
    hs = fft(ys)
    fs = fftfreq(n, d) # period
    # attenuate frequences below cutoff
    hs[abs(fs) < cutoff] *= factor
    new_ys = ifft(hs)
    return new_ys

def low_pass(ys, cutoff, factor=0, framerate=44100):
    """
    Attenuate frequencies above the cutoff.

    ys -- the wave (numpy array)
    cutoff -- frequency (Hz)
    factor -- what to multiply the magnitude by
    framerate -- framerate of wave
    """
    n = len(ys)
    d = 1 / framerate # period
    hs = fft(ys)
    fs = fftfreq(n, d)
    # attenuate frequences above cutoff
    hs[abs(fs) > cutoff] *= factor
    new_ys = ifft(hs)
    return new_ys

def band_filter(ys, lcutoff, hcutoff, factor=0, framerate=44100, stop=False):
    """
    Attenuates depending on whether one wants to band pass or stop
    1) Pass: Attenuate frequencies below and above the low and high cutoff frequencies
    2) Stop: Attenuate frequencies above and below the low and high cutoff frequencies

    ys -- the wave (numpy array)
    lcutoff -- low frequency (Hz)
    hcutoff -- high frequency (Hz)
    factor -- what to multiply the magnitude by
    framerate -- framerate of wave
    stop -- performs band stop if True otherwise band pass
    """
    n = len(ys)
    d = 1 / framerate # period
    hs = fft(ys)
    fs = abs(fftfreq(n, d))
    cutoff_indices = (lcutoff < fs) & (fs < hcutoff) if stop else \
                     (lcutoff > fs) & (fs > hcutoff)
    hs[cutoff_indices] *= factor
    new_ys = ifft(hs)
    return new_ys

def combine(a, b):
    """
    Combaines two Python lists into a numpy array

    a -- first list
    b -- second list
    """
    c = np.zeros(max(len(a), len(b)))
    if len(a) < len(b):
        c = b.copy()
        c[:len(a)] += a
    else:
        c = a.copy()
        c[:len(b)] += b
    return c

def beats_to_sec(b=QUARTER, bpm=60):
    """
    Seconds per beat
    
    b -- a single quarter note or another note length
    """
    # 1/BPM -> minutes / beat
    # (minutes / beat) * 60 -> seconds / beat
    return b * (1/bpm) * 60.0


def beats_to_samples(b=QUARTER, bpm=60, fr=44100):
    """
    Seconds per beat
    
    b -- a single quarter note or another note length
    """
    # 1/BPM -> minutes / beat
    # (minutes / beat) * 60 -> seconds / beat
    # 
    return beats_to_sec(b, bpm) * fr

