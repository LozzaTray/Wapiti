"""code to generate wav from file"""
from src.audio.recording import Recording
from config import N, K, C, D, W, Q, Q1, Q2, q, F, F0, F1
from src.file_io.utils import get_data_file_path, get_recording_file_path
from src.coding.encode import encode_bit_string
from src.coding.utils import xor
from src.ofdm.modulate import modulate_sequence
from src.audio.chirp import generate_chirp_recording
import numpy as np
import math


def bits_to_ofdm_sequence(bit_string):
    print("Modulating bit pairs into constellation...")
    symbol_sequence = encode_bit_string(bit_string)
    print("Converting into time domain...")
    modulated_sequence = modulate_sequence(symbol_sequence, N=N, K=K, Q1=Q1, Q2=Q2)
    return modulated_sequence


def bits_to_wav_recording(data_bit_string, known_bit_string):
    P = N + K
    
    print("Generating chirp delimiter...")
    chirp_rec = generate_chirp_recording(F, F0, F1, C*P)

    print("Generating known OFDM block...")
    known_block = bits_to_ofdm_sequence(known_bit_string)
    known_block_repeated = np.tile(known_block, D)
    known_rec = Recording.from_list(known_block_repeated, F)

    print("Performing XOR of real data with bit_mask...")
    xored_string = xor(data_bit_string, N//2 - 1)

    print("Generating OFDM data sequence...")
    data_sequence = bits_to_ofdm_sequence(xored_string)

    # constructing packets
    num_blocks = len(data_sequence) // P
    num_packets = math.ceil(num_blocks / W)

    master_rec = Recording.empty(F)
    master_rec.append_recording(chirp_rec)

    print("Splitting into packets...")
    for i in range(0, num_packets):
        lower_index = i*W*P
        upper_index = lower_index + W*P

        packet_data = data_sequence[lower_index : upper_index]
        
        # padding with repeat of first symbol
        num_data_blocks = len(packet_data) // P
        if(num_data_blocks < W):
            first_block = packet_data[0 : P]
            suffix = np.tile(first_block, W - num_data_blocks)
            packet_data = np.concatenate((packet_data, suffix))

        known_packet_known = np.concatenate((
            known_block_repeated,
            packet_data,
            known_block_repeated
        ))

        packet_data_rec = Recording.from_list(known_packet_known, F, rescale=True)

        master_rec.append_recording(packet_data_rec)
        master_rec.append_recording(chirp_rec)

    print("Done creating transmission")
    return master_rec


def create_bits_for_file(file_name, file_path):
    file_obj = open(file_path, mode="rb")
    source_bytes = file_obj.read()
    file_obj.close()
    
    file_length = str(len(source_bytes))

    zero_byte = "00000000"
    name_bit_string = "".join([format(ord(char), "08b") for char in file_name])
    length_bit_string = "".join([format(ord(str_num), "08b") for str_num in file_length])
    data_bit_string = "".join([format(byte, "08b") for byte in source_bytes])

    complete_bit_string = name_bit_string + zero_byte + length_bit_string + zero_byte + data_bit_string
    return complete_bit_string


def run():

    # get data pre-transmission
    source_file_name = input("File to encode (must be in data dir): ")
    #source_file_name = "elk.bmp"
    source_file_path = get_data_file_path(source_file_name)
    source_bits = create_bits_for_file(source_file_name, source_file_path)

    # known bits
    known_file = get_data_file_path("random_bits.txt")
    file_obj = open(known_file, mode="r")
    bits = file_obj.read()
    bit_mask = bits[0 : Q*q] # just sufficient for first symbol
    file_obj.close()

    # convert to wav
    rec = bits_to_wav_recording(source_bits, bit_mask)

    # save
    out_file_name = input("File name to save under (.wav): ")
    out_file_path = get_recording_file_path(out_file_name + ".wav")
    rec.save(out_file_path)


if __name__ == "__main__":
    print("\nTeam Wapiti - Encode File\n~~~~~~~~~~~~~~~~~~~\n")
    run()
