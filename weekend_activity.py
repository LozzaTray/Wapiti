"""Code for decoding data"""
from packages.parser import read_csv_as_array
from packages.ofdm import decode
from packages.output import write_to_file
import os

curr_dir = os.path.dirname(__file__)


def run():
    """main loop"""
    data_seq_file = os.path.join(curr_dir, "data/gr3file.csv")
    data_seq = read_csv_as_array(data_seq_file)

    channel_file = os.path.join(curr_dir, "data/gr3channel.csv")
    channel = read_csv_as_array(channel_file)

    decoded_sequence = decode(data_seq, channel)
    output_file = os.path.join(curr_dir, "output/wa1.txt")
    write_to_file(output_file, decoded_sequence)
    print(decoded_sequence)


if __name__ == "__main__":
    print("Team Wapiti - WA1")
    run()