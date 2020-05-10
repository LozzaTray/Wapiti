"""Code for decoding data"""
from packages.parser import read_csv_as_array
from packages.ofdm import demodulate
from packages.output import write_to_file
from packages.decoder import decode_symbol_sequence
import os

curr_dir = os.path.dirname(__file__)


def run():
    """main loop"""
    data_seq_file = os.path.join(curr_dir, "data/gr3file.csv")
    data_seq = read_csv_as_array(data_seq_file)

    channel_file = os.path.join(curr_dir, "data/gr3channel.csv")
    channel = read_csv_as_array(channel_file)

    output_demod_file = os.path.join(curr_dir, "output/demodulated.txt")
    demodulated_sequence = demodulate(data_seq, channel)
    write_to_file(output_demod_file, demodulated_sequence)
    #demodulated_sequence = read_csv_as_array(output_demod_file)


    output_file = os.path.join(curr_dir, "output/decoded.txt")
    decoded_sequence = decode_symbol_sequence(demodulated_sequence)
    print(decoded_sequence)
    write_to_file(output_file, decoded_sequence)


if __name__ == "__main__":
    print("Team Wapiti - WA1")
    run()