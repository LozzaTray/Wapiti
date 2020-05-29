from src.audio.recording import Recording
from src.file_io.utils import get_data_file_path
from src.ofdm.estimate_channel import estimate_channel
from src.ofdm.demodulate import demodulate_sequence
from src.coding.decode import decode_symbol_sequence
from src.coding.utils import xor
from src.file_io.jossy_format import perform_jossy
from src.audio.chirp import generate_chirp_recording
from config import N, K, F, F0, F1, C, D
from src.file_io.utils import progress_bar
from src.file_io.jossy_format import decode_bit_string_jossy_format_and_save
from src.ofdm.known_data import gen_known_data_chunk
from src.plotting.impulse_response import plot_h_in_time

def run():
    P = N + K
    print("Loading Recording...")
    signal_file = input("which file would you like to decode? (no .wav required) ")
    signal_file = get_data_file_path(signal_file + ".wav")
    signal_rec = Recording.from_file(signal_file)
    
    print("extracting packets")
    chirp_rec = generate_chirp_recording(F, F0, F1, C*P)
    packet_arr, dither_arr = signal_rec.extract_packets(chirp_rec)

    num_packets = len(packet_arr)
    print("\nPackets found: {}\n".format(num_packets))

    data_sequence = ""
    num_steps = 3
    print("Decoding packets")
    for i in range(0, num_packets):
        packet = packet_arr[i]
        dither = dither_arr[i]

        #slicing key data
        known_data_at_start = packet[0 : D * P]
        known_data_at_end = packet[- D * P : ]
        packet_data = packet[D * P : - D * P]

        #estimate channel at start
        known_data_pre_trans = gen_known_data_chunk(N, K)
        h_a = estimate_channel(known_data_at_start, known_data_pre_trans, N, K)
        h_b = estimate_channel(known_data_at_end, known_data_pre_trans, N, K)
        plot_h_in_time(h_a)
        plot_h_in_time(h_b)

        #demodulate
        progress_bar(i*num_steps, num_packets*num_steps)
        demodulated_signal = demodulate_sequence(packet_data, h_a, N, K)

        #decode
        progress_bar(i*num_steps + 1, num_packets*num_steps)
        decoded_signal = decode_symbol_sequence(demodulated_signal) #slowest step by far

        #xor
        progress_bar(i*num_steps + 2, num_packets*num_steps)
        de_xored = xor(decoded_signal, N//2 - 1)
        data_sequence = data_sequence + de_xored

    progress_bar(num_packets*num_steps, num_packets*num_steps)
    decode_bit_string_jossy_format_and_save(data_sequence)


if __name__ == "__main__":
    print("\nTeam Wapiti - decode transmission\n~~~~~~~~~~~~~~~~~~~\n")
    run()
