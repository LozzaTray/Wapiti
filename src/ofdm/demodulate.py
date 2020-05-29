"""Module for performing ofdm tasks"""
from src.ofdm.utils import dft, pad_so_divisible
import numpy as np


def demodulate_block(block, H_arr, N, K, Q1, Q2):
    """
    demodulates a single block
        block: complex[] length N+K
        H_arr: complex[] length N
    """
    
    if len(H_arr) != N:
        raise ValueError("Channel response length does not match N")

    if (len(block) != N + K):
        raise ValueError("Block length does not match N + K")

    # discard cyclic prefix
    sliced_block = block[K:]

    # take dft of block without cyclic pref
    dfted_block = dft(sliced_block, N)
    demodulated_block = np.divide(dfted_block, H_arr)

    # only take positive frequency bins
    relevant_bins = demodulated_block[Q1: Q2]
    return relevant_bins


def demodulate_sequence(received_sequence, channel_impulse_response_start, channel_impulse_response_end, N, K, Q1, Q2):
    """decodes by taking the DFT of the received_sequence and channel_impulse_response
    then apply point-wise division to get the true symbol value"""

    if (N % 2 != 0):
        raise ValueError("N must be an even integer")

    H_start = dft(channel_impulse_response_start, N)
    H_end = dft(channel_impulse_response_end, N)

    P = N + K
    padded_sequence = pad_so_divisible(received_sequence, P)
    sequence_length = len(padded_sequence)
    num_blocks = int(sequence_length / P)

    demodulated_sequence = []

    for i in range(0, num_blocks):
        lower_index = i * P
        upper_index = lower_index + P
        H_arr_block = H_start + (H_end - H_start)*i/num_blocks

        block = padded_sequence[lower_index : upper_index]
        demodulated_block = demodulate_block(block, H_arr_block, N, K, Q1, Q2)


        demodulated_sequence = np.concatenate((demodulated_sequence, demodulated_block))

    return demodulated_sequence
