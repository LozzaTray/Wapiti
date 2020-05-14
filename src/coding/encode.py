"""Module for encoding into QPSK"""
import numpy


def encode_bits(two_bits):
    """
    Checks argument and or magnitude and returns
    """
    if two_bits[0] == 0:
        if two_bits[1] == 0:
            return complex(1, 1)
        else:
            return complex(-1, 1)
    elif two_bits[1] == 0:
        return complex(1, -1)
    else:
        return complex(-1, -1)


def encode_bit_sequence(bit_sequence):
    """
    encodes a bit sequence into an array of complex symbols
    """
    # make sure the bit sequence is flattened just in case
    try:
        bits = bit_sequence.flatten()
    except:
        AttributeError
        bits = bit_sequence

    # bits = bit_sequence
    # check length of bits is even
    if len(bits) % 2 != 0:
        raise ValueError("bit sequence must be an even number of bits!")

    symbol_sequence = []
    i = 0
    while i < len(bit_sequence):
        symbol_sequence.append(encode_bits(bits[i:i + 2]))
        i += 2

    return symbol_sequence
