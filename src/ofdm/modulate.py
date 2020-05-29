"""Module for performing ofdm tasks"""
from src.ofdm.utils import idft, pad_so_divisible, insert_cyclic_prefix
import numpy as np


def modulate_block(block, N, K, Q1, Q2):
    """
    encodes the data_sequence X into the the time sequence x 
    by taking the iDFT and inserting a cyclic prefix of length K
    """

    # check block is of correct length
    M = (N // 2) - 1
    Q = Q2 - Q1
    main_block = block
    lower_block = block[0 : Q1] # length Q1
    upper_block = block[0 : M - Q2] #length M - Q2
    expanded_block = np.concatenate((lower_block, main_block, upper_block))

    if (len(expanded_block) != M):
        raise ValueError("Block is incorrect length")

    # manipulate block to produce real output
    reverse_conjugate_block = np.conjugate(np.flip(expanded_block))
    modified_block = np.concatenate((
        [0],
        expanded_block,
        [0],
        reverse_conjugate_block
    ))
    
    # take dft and prepend cyclic prefix
    x = idft(modified_block, N)
    x_cyclic = insert_cyclic_prefix(x, K)
    return x_cyclic


def modulate_sequence(data_sequence, N, K, Q1, Q2):
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
        modulated_block = modulate_block(block, N, K, Q1, Q2)
        modulated_sequence = np.concatenate((modulated_sequence, modulated_block))

    real_part = np.real_if_close(modulated_sequence)
    return real_part