"""Module for decoding"""
import numpy
import math
from functools import reduce


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
    decodes the symbol sequence, output of the form 'xxx...xxx'
    """
    bit_map = map(decode_symbol, symbol_sequence)
    bit_list = list(bit_map)  
    bits = reduce(lambda x, y: x + y, bit_list)
    return bits
