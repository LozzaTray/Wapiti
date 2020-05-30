"""code to generate wav from file"""
from src.audio.recording import Recording
from config import N, get_K, C, D, W, Q, Q1, Q2, q, F, F0, F1
from src.file_io.utils import get_data_file_path, get_recording_file_path
from src.coding.encode import encode_bit_string
from src.coding.utils import xor
from src.ofdm.modulate import modulate_sequence
from src.audio.chirp import generate_chirp_recording
from src.ofdm.known_data import gen_known_data_chunk
from src.file_io.utils import progress_bar
import numpy as np
import math


def bits_to_ofdm_sequence(bit_string, K):
    symbol_sequence = encode_bit_string(bit_string)
    modulated_sequence = modulate_sequence(symbol_sequence, N=N, K=K, Q1=Q1, Q2=Q2)
    return modulated_sequence


def bits_to_wav_recording(data_bit_string, K):
    P = N + K
    
    print("Generating chirp delimiter...")
    chirp_rec = generate_chirp_recording(F, F0, F1, C*P)

    print("Generating known OFDM block...")
    known_block_repeated = gen_known_data_chunk(N, K)

    bits_per_packet = Q * q * W
    num_bits = len(data_bit_string)
    num_packets = math.ceil(num_bits / bits_per_packet)

    print("Initialising empty recording...")
    master_rec = Recording.empty(F)
    master_rec.append_recording(chirp_rec)

    num_steps = 3
    print("Splitting into {} packets...".format(num_packets))
    for i in range(0, num_packets):
        lower_index = i * bits_per_packet
        upper_index = lower_index + bits_per_packet

        #slice
        packet_bits = data_bit_string[lower_index : upper_index]

        #xor
        progress_bar(i*num_steps, num_packets*num_steps)
        xored_bits = xor(packet_bits, Q*q)

        #convert to time domain
        progress_bar(i*num_steps + 1, num_packets*num_steps)
        packet_data_ofdm = bits_to_ofdm_sequence(xored_bits, K)
        
        # padding with repeat of first symbol
        num_data_blocks = len(packet_data_ofdm) // P
        if(num_data_blocks < W):
            first_block = packet_data_ofdm[0 : P]
            suffix = np.tile(first_block, W - num_data_blocks)
            packet_data_ofdm = np.concatenate((packet_data_ofdm, suffix))

        #concatenation
        progress_bar(i*num_steps + 2, num_packets*num_steps)
        known_packet_known = np.concatenate((
            known_block_repeated,
            packet_data_ofdm,
            known_block_repeated
        ))

        packet_data_rec = Recording.from_list(known_packet_known, F, rescale=True)

        master_rec.append_recording(packet_data_rec)
        master_rec.append_recording(chirp_rec)

    progress_bar(1, 1)
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
    # get mode
    mode = input("Transmission mode: ")
    K = get_K(mode)

    # get data pre-transmission
    source_file_name = input("File to encode (must be in data dir): ")
    
    #source_file_name = "elk.bmp"
    source_file_path = get_data_file_path(source_file_name)
    source_bits = create_bits_for_file(source_file_name, source_file_path)

    # convert to wav
    rec = bits_to_wav_recording(source_bits, K)

    # save
    out_file_name = input("File name to save under (.wav): ")
    out_file_path = get_recording_file_path(out_file_name + ".wav")
    rec.save(out_file_path)


if __name__ == "__main__":
    print("\nTeam Wapiti - Encode File\n~~~~~~~~~~~~~~~~~~~\n")
    run()
