"""code to generate artificial recording for transmitting known data"""
from src.audio.recording import Recording
from src.ofdm.modulate import modulate_sequence
from src.ofdm.demodulate import demodulate_sequence
from src.coding.encode import encode_bit_string
from src.coding.decode import decode_symbol_sequence
from src.coding.utils import text_to_bin
from src.plotting.plot_recording import plot_recording
from src.file_io.utils import get_output_file_path
from src.ofdm.estimate_channel import estimate_channel, plot_H_in_time, plot_H_freq_domain
from config import SAMPLING_FREQ
import numpy as np



def run():
    """main loop"""
    sent_file = input("Data that was sent (.wav): ")
    sent_file = get_output_file_path(sent_file + ".wav")
    data_rec = Recording.from_file(sent_file)
    
    data_seq = data_rec.get_frames_as_int16()
    D = len(data_seq)
    

    received_file = input("Recorded transmission (.wav): ")
    received_file = get_output_file_path(received_file + ".wav")
    received_rec = Recording.from_file(received_file)


    reference_file = input("Reference signal (.wav): ")
    reference_file = get_output_file_path(reference_file + ".wav")
    reference_rec = Recording.from_file(reference_file)

    received_data = received_rec.extract_data_sequence(reference_rec, D)

    H = estimate_channel(received_data, data_seq, N=1024, K=1000)

    plot_H_in_time(H, N=1024)
    plot_H_freq_domain(H)



if __name__ == "__main__":
    print("\nTeam Wapiti - Creating Data\n~~~~~~~~~~~~~~~~~~~\n")
    run()
