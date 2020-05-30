from src.ofdm.demodulate import demodulate_sequence
from src.file_io.utils import get_output_file_path
import numpy as np
from src.coding.decode import decode_symbol
import math
from config import q


def perform_jossy(data_sequence, impulse_response, N, K):
    """Decodes a data array according to Jossy format"""
    print("Demodulating OFDM...")
    symbol_sequence = demodulate_sequence(data_sequence, impulse_response, N=N, K=K)

    print("Decoding QPSK...")
    title, file_length, file_bytes = decode_symbol_sequence_jossy_format(symbol_sequence)

    print("Successfully decoded: " + title + " (" + str(file_length) + " bytes)")
    
    print("Saving file...")
    output_file = get_output_file_path(title)
    file_bytes.tofile(output_file)


def bit_array_to_byte(bits_array):
    """
    Convert an array of bit strings of unkown length into a byte
    """

    byte = ""
    for bits in bits_array:
        byte = byte + str(bits)

    if len(byte) != 8:
        raise ValueError("Supplied array does not comprise 8")

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


def decode_symbol_sequence_jossy_format(symbol_sequence):
    """
    decodes the symbol sequence
    symbol_sequence: complex[]
    returns: title (str), file_length (int), file_bytes (byte[])
    """

    symbols_per_byte = 8 // q
    decoded_sequence = np.array(list(map(decode_symbol, symbol_sequence)))
    
    num_symbols_long = len(decoded_sequence)
    num_bytes = math.floor(num_symbols_long / symbols_per_byte)

    decoded_sequence = decoded_sequence[0: num_bytes * symbols_per_byte]

    byte_sequence = np.reshape(decoded_sequence, (num_bytes, symbols_per_byte))
    byte_sequence = np.array(list(map(bit_array_to_byte, byte_sequence))).astype("uint8")
    
    return parse_byte_sequence(byte_sequence)


def decode_bit_string_jossy_format_and_save(bit_string):
    """
    decodes the supplied bit sequence and saves
    accepts:
        bit_string: str = "10011101"
    """
    bits_per_byte = 8
    num_bits_long = len(bit_string)
    num_bytes = math.floor(num_bits_long / bits_per_byte)

    bit_string = bit_string[0: num_bytes * bits_per_byte]

    byte_sequence = [ bit_string[ i : i + bits_per_byte] for i in range(0, num_bytes * bits_per_byte, bits_per_byte) ]
    byte_sequence = np.array(list(map(bit_array_to_byte, byte_sequence))).astype("uint8")

    print("Saving raw bytes to output/raw.bin")
    raw_out_file = get_output_file_path("raw.bin")
    byte_sequence.tofile(raw_out_file)
    
    try:
        title, file_length, file_bytes = parse_byte_sequence(byte_sequence)

        print("Successfully decoded: " + title + " (" + str(file_length) + " bytes)")
        
        print("Saving file...")
        output_file = get_output_file_path(title)
        file_bytes.tofile(output_file)

    except Exception as e:
        print(e)
        print("\n#######################\n- File Header damaged -\n#######################\n")
        print("Check output/raw.bin for raw bytes")