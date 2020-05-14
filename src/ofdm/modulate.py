"""Module for performing ofdm tasks"""
from src.ofdm.utils import idft, pad_so_divisible, insert_cyclic_prefix
import numpy as np


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
        block = padded_sequence[lower_index : upper_index]
        modulated_block = modulate_block(block, N, K)
        modulated_sequence = np.concatenate((modulated_sequence, modulated_block))

    return np.real_if_close(modulated_sequence)