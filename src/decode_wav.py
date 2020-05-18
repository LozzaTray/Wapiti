"""code to generate artificial recording for transmitting known data"""
from src.audio.recording import Recording
from src.ofdm.modulate import modulate_sequence
from src.ofdm.demodulate import demodulate_sequence
from src.coding.encode import encode_bit_string
from src.coding.decode import decode_symbol_sequence
from src.coding.utils import text_to_bin
from src.plotting.plot_recording import plot_recording
from src.file_io.utils import get_output_file_path
from src.ofdm.estimate_channel import estimate_channel, plot_H_in_time
from config import SAMPLING_FREQ



def run():
    """main loop"""
    # dummy data
    data = text_to_bin("Wapiti")
    #data = format(1530, '016b')
    print(data)
    # making a long data file
    for i in range(10):
        data += data
    print("data fully created")

    # doing the encoding and modulation
    QPSK = encode_bit_string(data)
    print("data encoded into QPSK")
    modulated_data = modulate_sequence(QPSK, N=1024, K=1000)
    print("QPSK data modulated; ready for playback")
    scaling = (2**15 -1)/max(abs(modulated_data))
    sent_data = scaling * modulated_data
    D = len(sent_data)

    received_file = input("Recorded transmission (.wav): ")
    received_file = get_output_file_path(received_file + ".wav")

    received_rec = Recording.from_file(received_file)

    reference_file = input("Reference signal (.wav): ")
    reference_file = get_output_file_path(reference_file + ".wav")
    reference_rec = Recording.from_file(reference_file)

    received_data = received_rec.extract_data_sequence(reference_rec, D)
    H = estimate_channel(received_data, sent_data, N=1024, K=1000)
    plot_H_in_time(H[3], N=1024)



if __name__ == "__main__":
    print("\nTeam Wapiti - Creating Data\n~~~~~~~~~~~~~~~~~~~\n")
    run()
