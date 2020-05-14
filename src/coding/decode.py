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
            symbol = [0, 0]
        else:
            symbol = [0, 1]
    else:
        if real >= 0:
            symbol = [1, 0]
        else:
            symbol = [1, 1]
    
    return symbol
