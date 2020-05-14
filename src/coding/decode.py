"""Module for decoding"""
import numpy
import math


def decode_symbol(complex_symbol):
    """
    Checks argument and or magnitude and returns
    """

    real = numpy.real(complex_symbol)
    imag = numpy.imag(complex_symbol)

    if imag >= 0:
        if real >= 0:
            symbol = b'00'
        else:
            symbol = b'01'
    else:
        if real >= 0:
            symbol = b'10'
        else:
            symbol = b'11'
    
    return symbol


def decode_symbol_sequence(symbol_sequence):
    """
    decodes the symbol sequence, output of the form b'xxx...xxx'
    """

    bits = b''
    bit_sequence = numpy.array(list(map(decode_symbol, symbol_sequence)))

    for i in range(len(bit_sequence)):
        bits += bit_sequence[i]

    return bits
