"""Module for decoding"""
import numpy


def map_symbol_to_bits(complex_symbol):
    """Checks argument and or magnitude and returns"""
    arg = numpy.angle(complex_symbol, deg=True)
    mag = numpy.abs(complex_symbol)
    if mag < 0.05: symbol = 2
    elif (arg >= 0) and (arg <= 90): symbol = [0, 0]
    elif (arg >= 90) and (arg <= 180): symbol = [0, 1]
    elif (arg <= 0) and (arg >= -90): symbol = [1, 1]
    elif (arg <= 90) and (arg >= -180): symbol = [1, 0]
    return symbol


def decode_until_zero_found(symbol_sequence, start_index=0):
    """loops through sequence until a two is found"""
    bit_sequence = []
    sequence_length = len(symbol_sequence)

    for i in range(start_index, sequence_length):
        symbol = symbol_sequence[i]
        decoded_bits = map_symbol_to_bits(symbol)
        if(decoded_bits != 2):
            bit_sequence = numpy.concatenate((bit_sequence, decoded_bits))
        else:
            print("Found a zero")
            return bit_sequence, decode_until_zero_found(symbol_sequence, i + 1)

    return bit_sequence


def decode_symbol_sequence(symbol_sequence):
    """takes whole sequence and maps to bits"""
    blocks = decode_until_zero_found(symbol_sequence)
    return blocks