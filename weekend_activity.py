"""Code for decoding data"""
from parser import read_csv_as_array
import os

curr_dir = os.path.dirname(__file__)


def run():
    """main loop"""
    data_seq_file = os.path.join(curr_dir, "/data/gr3file.csv")
    data_seq = read_csv_as_array(data_seq_file)

    channel_file = os.path.join(curr_dir, "/data/gr3channel.csv")
    channel = read_csv_as_array(channel_file)

    print(data_seq)
    print(channel)


if __name__ == "__main__":
    print("Team Wapiti - WA1")
    run()