"""Code for decoding data"""
from packages.parser import read_csv_as_array
from packages.ofdm import demodulate
from packages.output import write_binary, write_rows, write_bytes
from packages.decoder import decode_symbol_sequence
import os

curr_dir = os.path.dirname(__file__)


def run():
    """main loop"""
    print("Reading data file...")
    data_seq_file = os.path.join(curr_dir, "data/gr3file.csv")
    data_seq = read_csv_as_array(data_seq_file)

    print("Reading channel file...")
    channel_file = os.path.join(curr_dir, "data/gr3channel.csv")
    channel = read_csv_as_array(channel_file)

    print("OFDM demodulation...")
    #output_demod_file = os.path.join(curr_dir, "output/demodulated.txt")
    demodulated_sequence = demodulate(data_seq, channel)
    #write_rows(output_demod_file, demodulated_sequence)

    print("QPSK decoding...")
    output_file = os.path.join(curr_dir, "output/decoded.bin")
    decoded_bytes = decode_symbol_sequence(demodulated_sequence)
    decoded = decoded_bytes.astype('uint8')
    decoded.tofile(output_file)

    print("Extracting raw data...")
    raw_output_file = os.path.join(curr_dir, "output/raw.wav")
    raw_data = decoded[17 : 17 + 38638 + 1]
    raw_data.tofile(raw_output_file)


if __name__ == "__main__":
    print("Team Wapiti - WA1")
    run()