"""Code for creating a chirp"""
from src.audio.recording import Recording
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt


def generate_chirp_array_as_int16(duration, sampling_freq, f0, f1):
    """
    generates a chirp for specified duration:
        duration: num (seconds)
        sampling_freq: int (Hz)
        f0: int (Hz)
        f1: int (Hz)
    """

    t = np.linspace(0, duration, int(duration * sampling_freq))
    data = (scipy.signal.chirp(t, f0, duration, f1, method='linear', phi=0, vertex_zero=True)*(2**15 - 1)).astype(np.int16)
    scaled_data = (data*(2**15 - 1)).astype(np.int16)
    return scaled_data