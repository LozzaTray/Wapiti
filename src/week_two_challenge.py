"""Code for simulating a virtual channel"""
from src.audio.recording import Recording
from src.file_io.utils import get_data_file_path, get_output_file_path
from src.audio.chirp import generate_chirp_array_as_int16
from src.plotting.plot_recording import plot_correlation, plot_schmidl
from src.file_io.jossy_format import perform_jossy
from src.file_io.parser import read_csv_as_array
from src.ofdm.estimate_channel import estimate_channel
from src.plotting.impulse_response import plot_h_in_time, plot_h_freq_domain
from src.ofdm.modulate import modulate_schmidl_odd, modulate_sequence
from src.ofdm.utils import idft
import numpy as np
import numpy as np


def encode_two_bits(x):
    """returns QPSK symbol for value x"""
    if x == 0:
        return 1+1j
    elif x == 1:
        return -1+1j
    elif x == 3:
        return -1-1j
    elif x == 2:
        return 1-1j
    else:
        raise ValueError(r"Argument not in {0, 1, 2, 3}")


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

    print("Extracting sequence...")
    data_sequence = signal_rec.extract_data_sequence(chirp_rec, N*1000)
    data_sequence = data_sequence[ N+K : ] # discard first symbol used for synch

    perform_jossy(data_sequence, [1], N=N, K=K)
 

def q2():
    """Well this is a lot harder"""
    #constants
    N = 4096
    K = 0

    print("Loading Recording...")
    signal_file = "b8v89t_received"
    signal_file = get_data_file_path(signal_file + ".wav")
    signal_rec = Recording.from_file(signal_file)

    print("Loading known sequence...")
    data_file = get_data_file_path("a7r56tu_knownseq.csv")
    pre_modulation = read_csv_as_array(data_file)

    print("Performing schmidl modulation...")
    pre_modulation = pre_modulation[0 : N // 4]
    known_schmidl = modulate_schmidl_odd(pre_modulation, N=N, K=K)

    print("Extracting sequence...")
    data_sequence = signal_rec.extract_data_sequence_schmidl(N=N, K=K, D=N*1000, known_block=known_schmidl)

    print("Performing Jossy decoding")
    perform_jossy(data_sequence, [1], N=N, K=K)


def q3():
    """Well Alice..."""
    #constants
    RATE = 48000
    F0 = 100
    F1 = 8000
    T = 1
    N = 4096
    K = 100
    NUM_PILOTS = 100

    # other params
    P = N+K

    print("Loading Recording...")
    # file structure
    # chirp - sc - 100 x known - Data
    signal_file = "c9a71v_received"
    signal_file = get_data_file_path(signal_file + ".wav")
    signal_rec = Recording.from_file(signal_file)

    print("Generating Chirp...")
    chirp_arr = generate_chirp_array_as_int16(T, RATE, F0, F1)
    chirp_rec = Recording.from_list(chirp_arr, RATE)

    print("Extracting sequence after chirp...")
    offset = -10
    data_sequence = signal_rec.extract_data_sequence(chirp_rec, P*1000, offset=offset)
    data_sequence = data_sequence[ P : ] # discard first symbol used for schmidl

    print("Dividing into relevant chunks...")
    known_sequence = data_sequence[ : NUM_PILOTS * P]
    known_sequence = np.reshape(known_sequence, (NUM_PILOTS, P))
    known_sequence = np.mean(known_sequence, axis=0)
    ofdm_sequence = data_sequence[NUM_PILOTS * P :] # rest of data

    print("Loading known sequence...")
    data_file = get_data_file_path("a7r56tu_knownseq.csv")
    source_bits = read_csv_as_array(data_file)
    symbol_sequence = list(map(encode_two_bits, source_bits))

    print("Performing ofdm modulation...")
    known_modulated = modulate_sequence(symbol_sequence, N=N, K=K)
    #known_modulated = np.tile(known_modulated, NUM_PILOTS)

    print("Estimating channel...")
    h = estimate_channel(known_sequence, known_modulated, N, K)
    plot_h_in_time(h)
    plot_h_freq_domain(h, N=N)

    print("Let's be having ya...")
    perform_jossy(ofdm_sequence, h, N=N, K=K)



if __name__ == "__main__":
    print("\nTeam Wapiti - Week 2 Challenge\n~~~~~~~~~~~~~~~~~~~\n")
    #q1()
    #q2()
    q3()
