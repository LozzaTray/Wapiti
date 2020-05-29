from config import Q, q, D, Q1, Q2
from src.file_io.utils import get_data_file_path
from src.coding.encode import encode_bit_string
from src.ofdm.modulate import modulate_sequence
import numpy as np


def gen_known_data_chunk(N, K):
    """Generates the standard block"""
    known_file = get_data_file_path("random_bits.txt")
    
    file_obj = open(known_file, mode="r")
    bit_string = file_obj.read()
    bit_string = bit_string[0 : Q*q] # just sufficient for first symbol
    file_obj.close()

    # map to QPSK
    symbol_sequence = encode_bit_string(bit_string)
    # convert to time-domain
    known_block = modulate_sequence(symbol_sequence, N=N, K=K, Q1=Q1, Q2=Q2)
    
    # check just one block long
    P = N + K
    assert len(known_block) == P

    # repeat D times
    known_block_repeated = np.tile(known_block, D)
    return known_block_repeated