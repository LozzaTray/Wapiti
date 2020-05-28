from src.audio.recording import Recording
from src.file_io.utils import get_data_file_path
from src.ofdm.estimate_channel import estimate_channel
from src.ofdm.demodulate import demodulate_sequence
from src.coding.decode import decode_symbol_sequence
from src.coding.utils import xor
from src.file_io.jossy_format import perform_jossy
from config import N, K

def run():
    print("Loading Recording...")
    signal_file = input("which file would you like to decode? (no .wav required) ")
    signal_file = get_data_file_path(signal_file + ".wav")
    signal_rec = Recording.from_file(signal_file)
    """
    extract data sequence using file to be added    
    """
    print("estimating channel")
    channel_estimate = estimate_channel(received_signal, known_sequence, N=N, K=K)
    print("demodulating")
    demodulated_signal = demodulate_sequence(received_signal, channel_estimate, N, K)
    print("decoding")
    decoded_signal = decode_symbol_sequence(demodulated_signal)
    print("xor time")
    de_xored = xor(decoded_signal, N/2 - 1)
    print("jossy format")
    final = perform_jossy(de_xored)




if __name__ == "__main__":
    print("\nTeam Wapiti - decode transmission\n~~~~~~~~~~~~~~~~~~~\n")
    run()
