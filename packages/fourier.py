"""Module for performing fourier analysis"""

import numpy

def dft(data_vector):
    """
    Perform dft on the given data_vector
    Returns vector of length N
    """

    return numpy.fft.fft(data_vector)

    raise NotImplementedError


def idft(data_vector):
    """
    Performs inverse dft on the given data_vector
    Returns vector of length N
    """

    return numpy.fft.ifft(data_vector)

    raise NotImplementedError