"""Code for simulating a virtual channel"""
from src.audio.recording import Recording
from src.file_io.utils import get_data_file_path, get_output_file_path
from src.audio.chirp import generate_chirp_array_as_int16
from src.plotting.plot_recording import plot_correlation
from src.decode_csv import decode_symbol_sequence_jossy_format
from src.ofdm.demodulate import demodulate_sequence


def q1():
    """Question 1"""
    #constants
    RATE = 48000
    F0 = 100
    F1 = 8000
    T = 1
    N = 4096
    K = 0

    print("Loading Recording...")
    signal_file = "a7r56tu_received"
    signal_file = get_data_file_path(signal_file + ".wav")
    signal_rec = Recording.from_file(signal_file)

    print("Generating Chirp...")
    chirp_arr = generate_chirp_array_as_int16(T, RATE, F0, F1)
    chirp_rec = Recording.from_list(chirp_arr, RATE)

    #print("Testing Correlation...")
    #plot_correlation(signal_rec, chirp_rec)

    print("Extracting sequence...")
    data_sequence = signal_rec.extract_data_sequence(chirp_rec, N*1000)
    data_sequence = data_sequence[ N+K : ] # discard first symbol used for synch

    print("Demodulating OFDM...")
    symbol_sequence = demodulate_sequence(data_sequence, [1], N=N, K=K)

    print("Decoding QPSK...")
    title, file_length, file_bytes = decode_symbol_sequence_jossy_format(symbol_sequence)

    print("Successfully decoded: " + title + " (" + str(file_length) + " bytes)")
    
    print("Saving file...")
    output_file = get_output_file_path(title)
    file_bytes.tofile(output_file)
 

def q2():
    """Well this is a lot harder"""
    pass


if __name__ == "__main__":
    print("\nTeam Wapiti - Week 2 Challenge\n~~~~~~~~~~~~~~~~~~~\n")
    q1()
    #q2()
