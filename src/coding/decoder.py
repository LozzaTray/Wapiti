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


def bit_array_to_byte(bit_array):
    """
    Convert an array of 8-bits into a byte
    """

    if len(bit_array) != 8:
        raise ValueError("Supplied array was not length 8")

    byte = ""
    for bit in bit_array:
        byte = byte + str(bit)
    return int(byte, base=2)


def parse_byte_sequence(byte_sequence):
    """
    parses a byte sequence to retrieve the title, 
    file length in bytes and byte array corresponding to the file
    """

    title = ""
    file_length = ""

    num_bytes = len(byte_sequence)
    first_zero_index = 0
    second_zero_index = 0

    for i in range(0, num_bytes):
        byte = byte_sequence[i]
        if byte == 0:
            first_zero_index = i
            break
        else:
            title = title + chr(byte)

    for j in range(first_zero_index + 1, num_bytes):
        byte = byte_sequence[j]
        if byte == 0:
            second_zero_index = j
            break
        else:
            file_length = file_length + chr(byte)

    file_length = int(file_length)

    file_start_index = second_zero_index + 1
    file_bytes = byte_sequence[file_start_index : file_start_index + file_length]

    return title, file_length, file_bytes


def decode_symbol_sequence(symbol_sequence):
    """
    decodes the symbol sequence
    returns: title (str), file_length (int), file_bytes (byte[])
    """

    bit_sequence = numpy.array(list(map(decode_symbol, symbol_sequence)))
    bit_sequence = bit_sequence.flatten()
    
    num_bits = len(bit_sequence)
    num_bytes = math.floor(num_bits / 8)

    bit_sequence = bit_sequence[0: num_bytes * 8]

    byte_sequence = numpy.reshape(bit_sequence, (num_bytes, 8))
    byte_sequence = numpy.array(list(map(bit_array_to_byte, byte_sequence))).astype("uint8")
    
    return parse_byte_sequence(byte_sequence)