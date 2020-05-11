"""Module for performing ofdm tasks"""
from .fourier import dft, idft
import numpy as np


def insert_cyclic_prefix(x, K):
    """inserts a cyclic prefix of length K into the data sequence x
    allows linear convolution to match cyclic"""
    raise NotImplementedError


def modulate(data_sequence, K):
    """encodes the data_sequence X into the the time sequence x 
    by taking the iDFT and inserting a cyclic prefix of length K"""
    raise NotImplementedError


def demodulate(received_sequence, channel_impulse_response, N=1024, K=32):
    """decodes by taking the DFT of the received_sequence and channel_impulse_response
    then apply point-wise division to get the true symbol value"""
    H_arr = dft(channel_impulse_response, N)
    sequence_length = len(received_sequence)
    num_blocks = int(sequence_length / (N + K))

    decoded_sequence = []

    for i in range(0, num_blocks):
        # discard cyclic prefix
        lower_index = i*(N+K) + K
        upper_index = lower_index + N
        block = received_sequence[lower_index : upper_index]

        # take dft of block without cyclic pref
        dfted_block = dft(block, N)
        decoded_block = np.divide(dfted_block, H_arr)

        # only take positive frequency bins
        relevant_bins = decoded_block[1 : int(N/2)]

        #concatenate
        decoded_sequence = np.concatenate((decoded_sequence, relevant_bins))

    return decoded_sequence