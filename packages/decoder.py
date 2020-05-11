"""Module for decoding"""
import numpy


def map_symbol_to_bits(complex_symbol):
    """Checks argument and or magnitude and returns"""
    arg = numpy.angle(complex_symbol, deg=True)

    if (arg >= 0) and (arg <= 90):
        symbol = [0, 0]
    elif (arg >= 90) and (arg <= 180):
        symbol = [0, 1]
    elif (arg <= -90) and (arg >= -180):
        symbol = [1, 1]
    elif (arg <= 0) and (arg >= -90):
        symbol = [1, 0]
    
    return symbol


def decode_symbol_sequence(symbol_sequence):
    """loops through sequence until a two is found"""
    bit_sequence = numpy.array(list(map(map_symbol_to_bits, symbol_sequence)))
    bit_sequence = bit_sequence.flatten()
    return bit_sequence