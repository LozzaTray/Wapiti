"""Module for performing fourier analysis"""
import numpy as np


def dft(data_vector, N):
    """
    Perform N-point dft on the given data_vector
    Returns vector of length N
    """
    return np.fft.fft(data_vector, N)


def idft(data_vector, N):
    """
    Performs N-point inverse dft on the given data_vector
    Returns vector of length N
    """
    return np.fft.ifft(data_vector, N)


def pad_so_divisible(x, M):
    """pads x with zeros to length divisible M"""
    original_length = len(x)
    excess = original_length % M

    if(excess == 0):
        # already divisible
        return x

    padding = np.zeros(M - excess)
    arr = np.concatenate((x, padding))
    return arr


def insert_cyclic_prefix(x, K):
    """
    inserts a cyclic prefix of length K into the data sequence x
    makes linear convolution match cyclic convolution
    """
    if (K < 0):
        raise ValueError("Cyclic prefix-length must be non-negative")
    elif (K == 0) :
        return x
    else:
        x_cyclic = np.concatenate((x[-K:], x))
        return x_cyclic