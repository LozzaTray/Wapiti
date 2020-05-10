"""Module for performing fourier analysis"""

import numpy as np

def dft(data_vector):
    """
    Perform dft on the given data_vector
    Returns vector of length N
    """

    return np.fft.fft(data_vector)

    raise NotImplementedError


def idft(data_vector):
    """
    Performs inverse dft on the given data_vector
    Returns vector of length N
    """

    return np.fft.ifft(data_vector)

    raise NotImplementedError