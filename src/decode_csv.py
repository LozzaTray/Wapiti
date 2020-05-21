"""Code for decoding data"""
from config import DATA_DIR, OUTPUT_DIR
from src.file_io.parser import read_csv_as_array
from src.ofdm.demodulate import demodulate_sequence
from src.coding.decode import decode_symbol
import numpy as np
import math
import os


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

    symbols_per_byte = 4
    decoded_sequence = np.array(list(map(decode_symbol, symbol_sequence)))
    
    num_symbols_long = len(decoded_sequence)
    num_bytes = math.floor(num_symbols_long / symbols_per_byte)

    decoded_sequence = decoded_sequence[0: num_bytes * symbols_per_byte]

    byte_sequence = np.reshape(decoded_sequence, (num_bytes, symbols_per_byte))
    byte_sequence = np.array(list(map(bit_array_to_byte, byte_sequence))).astype("uint8")
    
    return parse_byte_sequence(byte_sequence)


def run():
    """main loop"""
    group = input("Which group are you: ")

    print("Reading data file...")
    data_seq_file = os.path.join(DATA_DIR, "gr" + group + "file.csv")
    data_seq = read_csv_as_array(data_seq_file)

    print("Reading channel file...")
    channel_file = os.path.join(DATA_DIR, "gr" + group + "channel.csv")
    channel = read_csv_as_array(channel_file)

    print("OFDM demodulation...")
    demodulated_sequence = demodulate_sequence(data_seq, channel)

    print("QPSK decoding...")
    title, file_length, file_bytes = decode_symbol_sequence_jossy_format(demodulated_sequence)
    print("Successfully decoded: " + title + " (" + str(file_length) + " bytes)")
    
    print("Saving file...")
    output_file = os.path.join(OUTPUT_DIR, title)
    file_bytes.tofile(output_file)

    print("Done")


if __name__ == "__main__":
    print("\nTeam Wapiti - WA1\n~~~~~~~~~~~~~~~~~~~\n")
    run()