"""Module for performing ofdm tasks"""
from src.ofdm.utils import idft, pad_so_divisible, insert_cyclic_prefix, scale_to_int16
from config import Q1, Q2
import numpy as np


def modulate_block(block, N, K):
    """
    encodes the data_sequence X into the the time sequence x 
    by taking the iDFT and inserting a cyclic prefix of length K
    """

    # check block is of correct length
    M = int((N / 2) - 1)
    Q = Q2 - Q1
    main_block = block
    lower_block = block[:Q1]
    upper_block = block[Q+Q2-M:]
    block = np.concatenate((lower_block, main_block, upper_block))

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


def modulate_sequence(data_sequence, N, K):
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

    M = Q2 - Q1
    padded_sequence = pad_so_divisible(data_sequence, M)
    sequence_length = len(padded_sequence)
    num_blocks = int(sequence_length / M)
    modulated_sequence = []

    for i in range(0, num_blocks):
        lower_index = i * M
        upper_index = lower_index + M
        block = padded_sequence[lower_index : upper_index]
        modulated_block = modulate_block(block, N, K)
        modulated_sequence = np.concatenate((modulated_sequence, modulated_block))

    real_part = np.real_if_close(modulated_sequence)
    scaled_sequence = scale_to_int16(real_part)
    return scaled_sequence


def modulate_schmidl_odd(data_sequence, N, K):
    """
    Performs an odd schmidl modulation on a data sequence
        data_sequence: num[]
        N: int
        K: int
    """
    d = len(data_sequence)
    out = np.zeros( 2 * d - 1)
    out[0 : len(out) : 2] = data_sequence # [start : stop : step] >> zeros at every odd index
    modulated_sequence = modulate_sequence(out, N, K)
    return modulated_sequence