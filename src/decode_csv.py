"""Code for decoding data"""
from config import DATA_DIR, OUTPUT_DIR
from src.file_io.parser import read_csv_as_array
from src.modulation.ofdm import demodulate_sequence
from src.file_io.output import write_binary, write_rows, write_bytes
from src.coding.decoder import decode_symbol_sequence
import os


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
    title, file_length, file_bytes = decode_symbol_sequence(demodulated_sequence)
    print("Successfully decoded: " + title + " (" + str(file_length) + " bytes)")
    
    print("Saving file...")
    output_file = os.path.join(OUTPUT_DIR, title)
    file_bytes.tofile(output_file)

    print("Done")


if __name__ == "__main__":
    print("\nTeam Wapiti - WA1\n~~~~~~~~~~~~~~~~~~~\n")
    run()