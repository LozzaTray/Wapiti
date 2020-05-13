"""Module for performing ofdm tasks"""
from src.modulation.fourier import dft, idft
import numpy as np
import math


def pad_so_divisible(x, M):
    """pads x with zeos to length divisible M"""
    original_length = len(x)
    excess = original_length % M

    if(excess == 0):
        # already divisible
        return x

    new_length = original_length + (M - excess)
    arr = np.zeros(new_length)
    arr[:original_length] = x
    return arr


def insert_cyclic_prefix(x, K):
    """
    inserts a cyclic prefix of length K into the data sequence x
    makes linear convolution match cyclic convolution
    """

    x_cyclic = np.concatenate((x[-K:], x))
    return x_cyclic


def modulate_block(block, N, K):
    """
    encodes the data_sequence X into the the time sequence x 
    by taking the iDFT and inserting a cyclic prefix of length K
    """

    # check block is of correct length
    M = int((N / 2) - 1)
    if (len(block) != M):
        raise ValueError("Block is incorrect length")

    # manipulate block to produce real output
    reverse_conjugate_block = np.conjugate(np.flip(block))
    modified_block = np.concatenate((
        [0],
        block,
        [0],
        reverse_conjugate_block
    ))
    
    # take dft and prepend cyclic prefix
    x = idft(modified_block, N)
    x_cyclic = insert_cyclic_prefix(x, K)
    return x_cyclic


def modulate_sequence(data_sequence, N=1024, K=32):
    """
    modulates given data sequence
    block length N
    prefix length K

    ensures output is real signal >> performs block

    returns:
    float[]
    """

    if(N % 2 != 0):
        raise ValueError("N must be an even integer")

    M = int((N/2) - 1)
    padded_sequence = pad_so_divisible(data_sequence, M)
    sequence_length = len(padded_sequence)
    num_blocks = int(sequence_length / M)
    modulated_sequence = []

    for i in range(0, num_blocks):
        lower_index = i * M
        upper_index = lower_index + M

        block = data_sequence[lower_index : upper_index]
        modulated_block = modulate_block(block, N, K)
        modulated_sequence = np.concatenate((modulated_sequence, modulated_block))

    return modulated_sequence


def demodulate_block(block, H_arr, N, K):
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
    relevant_bins = demodulated_block[1 : int(N/2)]
    return relevant_bins


def demodulate_sequence(received_sequence, channel_impulse_response, N=1024, K=32):
    """decodes by taking the DFT of the received_sequence and channel_impulse_response
    then apply point-wise division to get the true symbol value"""

    if (N % 2 != 0):
        raise ValueError("N must be an even integer")

    H_arr = dft(channel_impulse_response, N)

    P = N + K
    padded_sequence = pad_so_divisible(received_sequence, P)
    sequence_length = len(padded_sequence)
    num_blocks = int(sequence_length / P)

    demodulated_sequence = []

    for i in range(0, num_blocks):
        lower_index = i * P
        upper_index = lower_index + P
        
        block = received_sequence[lower_index : upper_index]
        demodulated_block = demodulate_block(block, H_arr, N, K)

        demodulated_sequence = np.concatenate((demodulated_sequence, demodulated_block))

    return demodulated_sequence
