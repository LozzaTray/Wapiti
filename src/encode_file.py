"""code to generate wav from file"""
from src.audio.recording import Recording
from config import N, K, C, D, W, Q, q, F, F0, F1
from src.file_io.utils import get_data_file_path, get_output_file_path
from src.coding.encode import encode_bit_string
from src.ofdm.modulate import modulate_sequence
from src.audio.chirp import generate_chirp_recording
import numpy as np
import math
from src.plotting.plot_recording import plot_recording


def bits_to_ofdm_sequence(bit_string):
    symbol_sequence = encode_bit_string(bit_string)
    modulated_sequence = modulate_sequence(symbol_sequence, N=N, K=K)
    return modulated_sequence


def bits_to_wav_recording(data_bit_string, known_bit_string):
    P = N + K
    
    # generate known block
    known_block = bits_to_ofdm_sequence(known_bit_string)
    known_block_repeated = np.tile(known_block, D)
    known_rec = Recording.from_list(known_block_repeated, F)

    # generate chirp
    chirp_rec = generate_chirp_recording(F, F0, F1, C*P)

    # generate data sequence
    data_sequence = bits_to_ofdm_sequence(data_bit_string)

    # constructing packets
    num_blocks = len(data_sequence) // P
    num_packets = math.ceil(num_blocks / W)

    master_rec = Recording.empty(F)
    master_rec.append_recording(chirp_rec)

    for i in range(0, num_packets):
        master_rec.append_recording(known_rec)

        lower_index = i*W*P
        upper_index = lower_index + W*P

        packet_data = data_sequence[lower_index : upper_index]
        packet_data_rec = Recording.from_list(packet_data, F)

        master_rec.append_recording(packet_data_rec)
        master_rec.append_recording(known_rec)
        master_rec.append_recording(chirp_rec)

    return master_rec
    


def run():

    # get data pre-transmission
    # source_file_name = input("File to encode (must be in data dir): ")
    source_file_name = "elk.bmp"
    source_file_path = get_data_file_path(source_file_name)
    file_obj = open(source_file_path, mode="rb")
    source_bits = file_obj.read()
    file_obj.close()

    # known bits
    known_file = get_data_file_path("random_bits.txt")
    file_obj = open(known_file, mode="r")
    bits = file_obj.read()
    bit_mask = bits[0 : Q*q] # just sufficient for first symbol
    file_obj.close()

    # convert to wav
    rec = bits_to_wav_recording(source_bits, bit_mask)
    plot_recording(rec)

    # optional save
    out_file_name = input("File name to save under (.wav): ")
    out_file_path = get_output_file_path(out_file_name + ".wav")
    rec.save(out_file_path)


if __name__ == "__main__":
    print("\nTeam Wapiti - Encode File\n~~~~~~~~~~~~~~~~~~~\n")
    run()
