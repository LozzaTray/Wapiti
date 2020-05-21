"""Code for simulating a virtual channel"""
from src.audio.recording import Recording
from src.file_io.utils import get_data_file_path, get_output_file_path
from src.audio.chirp import generate_chirp_array_as_int16
from src.plotting.plot_recording import plot_correlation, plot_schmidl
from src.file_io.jossy_format import perform_jossy


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
    RATE = 48000
    N = 4096
    K = 0

    print("Loading Recording...")
    signal_file = "b8v89t_received"
    signal_file = get_data_file_path(signal_file + ".wav")
    signal_rec = Recording.from_file(signal_file)

    print("Testing schmidl...")
    plot_schmidl(signal_rec, N=N)

    print("Extracting sequence...")
    #data_sequence = signal_rec.extract_data_sequence_schmidl(N*1000)
    #data_sequence = data_sequence[ N+K : ] # discard first symbol used for synch

    print("Performing Jossy decoding")
    #perform_jossy(data_sequence, [1], N=N, K=K)



if __name__ == "__main__":
    print("\nTeam Wapiti - Week 2 Challenge\n~~~~~~~~~~~~~~~~~~~\n")
    #q1()
    q2()
