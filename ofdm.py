"""Module for performing ofdm tasks"""
from fourier import DFT, iDFT
import numpy as np


def insert_cyclic_prefix(x, K):
    """inserts a cyclic prefix of length K into the data sequence x
    allows linear convolution to match cyclic"""
    raise NotImplementedError


def encode(data_sequence, K):
    """encodes the data_sequence X into the the time sequence x 
    by taking the iDFT and inserting a cyclic prefix of length K"""
    raise NotImplementedError


def decode(received_sequence, channel_impulse_response):
    """decodes by taking the DFT of the received_sequence and channel_impulse_response
    then apply point-wise division to get the true symbol value"""
    K = len(channel_impulse_response)
    N = len(received_sequence) - K

    H_arr = DFT(channel_impulse_response, N)
    Y_arr = DFT(received_sequence, N)

    Y_arr = Y_arr[K+1:]
    X_arr = np.divide(Y_arr, H_arr)

    return X_arr