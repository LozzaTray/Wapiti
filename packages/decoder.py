"""Module for decoding"""
import numpy


def map_symbol_to_bits(complex_symbol):
    """Checks argument and or magnitude and returns"""
    arg = numpy.angle(complex_symbol, deg=True)
    mag = numpy.abs(complex_symbol)
    if mag < 0.01: symbol = 2
    if (arg >= 0) and (arg <= 90): symbol = [0, 0]
    if (arg >= 90) and (arg <= 180): symbol = [0, 1]
    if (arg <= 0) and (arg >= -90): symbol = [1, 1]
    if (arg <= 90) and (arg >= -180): symbol = [1, 0]
    return symbol


def decode_symbol_sequence(symbol_sequence):
    """takes whole sequence and maps to bits"""
