"""Code for decoding data"""
from packages.parser import read_csv_as_array
from packages.ofdm import demodulate
from packages.output import write_binary, write_rows, write_bytes
from packages.decoder import decode_symbol_sequence
import os

curr_dir = os.path.dirname(__file__)


def run():
    """main loop"""
    group = input("Which group are you: ")

    print("Reading data file...")
    data_seq_file = os.path.join(curr_dir, "data/gr" + group + "file.csv")
    data_seq = read_csv_as_array(data_seq_file)

    print("Reading channel file...")
    channel_file = os.path.join(curr_dir, "data/gr" + group + "channel.csv")
    channel = read_csv_as_array(channel_file)

    print("OFDM demodulation...")
    demodulated_sequence = demodulate(data_seq, channel)

    print("QPSK decoding...")
    title, file_length, file_bytes = decode_symbol_sequence(demodulated_sequence)
    print("Successfully decoded: " + title + " (" + str(file_length) + " bytes)")
    
    print("Saving file...")
    output_file = os.path.join(curr_dir, "output/" + title)
    file_bytes.tofile(output_file)

    print("Done")


if __name__ == "__main__":
    print("\nTeam Wapiti - WA1\n~~~~~~~~~~~~~~~~~~~\n")
    run()