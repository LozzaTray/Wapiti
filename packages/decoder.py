"""Module for decoding"""
import numpy
import math


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


def map_bit_array_to_byte(bit_array):
    byte = ""
    for bit in bit_array:
        byte = byte + str(bit)
    return int(byte, base=2)


def decode_symbol_sequence(symbol_sequence):
    """loops through sequence until a two is found"""
    bit_sequence = numpy.array(list(map(map_symbol_to_bits, symbol_sequence)))
    bit_sequence = bit_sequence.flatten()
    
    num_bits = len(bit_sequence)
    num_bytes = math.floor(num_bits / 8)
    byte_sequence = numpy.reshape(bit_sequence[0: num_bytes * 8], (num_bytes, 8))
    byte_sequence = numpy.array(list(map(map_bit_array_to_byte, byte_sequence)))
    return byte_sequence.astype("uint8")