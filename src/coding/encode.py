"""Module for encoding into QPSK"""
import numpy


def encode_bits(two_bits):
    """
    encodes a length 2 bit string into 1 QPSK symbol
    """
    if two_bits[0:1] == b'0':
        if two_bits[1:2] == b'0':
            return complex(1, 1)
        else:
            return complex(-1, 1)
    elif two_bits[1:2] == b'0':
        return complex(1, -1)
    else:
        return complex(-1, -1)


def encode_bit_string(bit_sequence):
    """
    encodes a bit string into an array of complex symbols; takes input of the form b'xxx...xxx'
    """

    # check length of bits is even
    if len(bit_sequence) % 2 != 0:
        raise ValueError("bit sequence must be an even number of bits!")

    symbol_sequence = []
    i = 2
    while i < len(bit_sequence):
        symbol_sequence.append(encode_bits(bit_sequence[i:i + 2]))
        i += 2

    return symbol_sequence