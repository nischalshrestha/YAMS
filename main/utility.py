"""
This contains useful functions
"""

from constants import *
import scipy as sc
import numpy as np
from numpy.fft import fft
from numpy.fft import fftfreq
from numpy.fft import ifft

def combine(a, b):
    """
    Combines two Python lists into a numpy array

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

