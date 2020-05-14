"""Module for encoding into QPSK"""
import numpy


def encode_bits(two_bits):
    """
    Checks argument and or magnitude and returns
    """
    if two_bits[:1] == b'0':
        if two_bits[1:2] == b'0':
            return complex(1, 1)
        else:
            return complex(-1, 1)
    elif two_bits[1:2] == b'0':
        return complex(1, -1)
    else:
        return complex(-1, -1)


def encode_bit_sequence(bit_sequence):
    """
    encodes a bit sequence into an array of complex symbols; takes input of the form b'xxx...xxx'
    """
    # bits = bit_sequence
    # check length of bits is even
    if len(bit_sequence) % 2 != 0:
        raise ValueError("bit sequence must be an even number of bits!")

    symbol_sequence = []
    i = 0
    while i < len(bit_sequence):
        symbol_sequence.append(encode_bits(bit_sequence[i:i + 2]))
        i += 2

    return symbol_sequence
