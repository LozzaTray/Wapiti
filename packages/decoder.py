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


def decode_until_zero_found(symbol_sequence, start_index=0):
    """loops through sequence until a two is found"""
    bit_sequence = []
    sequence_length = len(symbol_sequence)
    zero_index = 0

    for i in range(start_index, sequence_length):
        symbol = symbol_sequence[i]
        decoded_bits = map_symbol_to_bits(symbol)
        if(decoded_bits != 2):
            bit_sequence.append(decoded_bits)
        else:
            zero_index = i
            break

    return bit_sequence, zero_index


def decode_symbol_sequence(symbol_sequence):
    """takes whole sequence and maps to bits"""
    title, zero_index = decode_until_zero_found(symbol_sequence)
    file_length, next_zero_index = decode_until_zero_found(symbol_sequence, zero_index + 1)
    data_sequence, discard = decode_until_zero_found(symbol_sequence, next_zero_index + 1)

    return title, file_length, data_sequence
