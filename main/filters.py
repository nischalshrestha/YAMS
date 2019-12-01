import scipy as sc
import numpy as np
from numpy.fft import fft
from numpy.fft import fftfreq
from numpy.fft import ifft

def high_pass(ys, cutoff, factor=0.1, framerate=44100, duration=1.0):
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

def low_pass(ys, cutoff, factor=0.1, framerate=44100, duration=1.0):
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

def band_filter(ys, lcutoff, hcutoff, factor=0.1, framerate=44100, stop=False):
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

def butter_low(wave, cutoff, N=2, fr=44100):
    b, a = sc.signal.butter(N, cutoff, fs=fr)
    return sc.signal.filtfilt(b, a, wave)

def butter_high(wave, cutoff, N=2, fr=44100):
    b, a = sc.signal.butter(N, cutoff, btype='high', fs=fr)
    return sc.signal.filtfilt(b, a, wave)

def butter_band(wave, lowcutoff, highcutoff, N=2, fr=44100):
    b, a = sc.signal.butter(N, [lowcutoff, highcutoff], btype='band', fs=fr)
    return sc.signal.filtfilt(b, a, wave)

