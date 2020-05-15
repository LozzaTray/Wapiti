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
            symbol = format(0, '02b')
        else:
            symbol = format(1, '02b')
    else:
        if real >= 0:
            symbol = format(2, '02b')
        else:
            symbol = format(3, '02b')
    
    return symbol


def decode_symbol_sequence(symbol_sequence):
    """
    decodes the symbol sequence, output of the form b'xxx...xxx'
    """

    bit_sequence = numpy.array(list(map(decode_symbol, symbol_sequence)))
    bits = bit_sequence[0]
    for i in range(len(bit_sequence)-1):
        bits += bit_sequence[i+1]

    return bits
