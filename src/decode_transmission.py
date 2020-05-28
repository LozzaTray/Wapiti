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
    print("Decoding packets")
    for i in range(0, num_packets):
        progress_bar(i+1, num_packets)
        packet = packet_arr[i]
        dither = dither_arr[i]

        #slicing key data
        known_data_at_start = packet[0 : D * P]
        known_data_at_end = packet[- D * P : ]
        packet_data = packet[D * P : - D * P]

        #estimate channel at start
        h_a = [1] #estimate_channel TODO
        h_b = [1] #estimate channel TODO

        demodulated_signal = demodulate_sequence(packet_data, h_a, N, K)
        decoded_signal = decode_symbol_sequence(demodulated_signal)
        de_xored = xor(decoded_signal, N//2 - 1)
        data_sequence = data_sequence + de_xored

    print(data_sequence)
    
    # print("estimating channel")
    # channel_estimate = estimate_channel(received_signal, known_sequence, N=N, K=K)
    # print("demodulating")
    # demodulated_signal = demodulate_sequence(received_signal, channel_estimate, N, K)
    # print("decoding")
    # decoded_signal = decode_symbol_sequence(demodulated_signal)
    # print("xor time")
    # de_xored = xor(decoded_signal, N//2 - 1)
    # print("jossy format")
    # final = perform_jossy(de_xored)




if __name__ == "__main__":
    print("\nTeam Wapiti - decode transmission\n~~~~~~~~~~~~~~~~~~~\n")
    run()
