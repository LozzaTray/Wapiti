"""code to generate artificial recording for transmitting known data"""
from src.audio.recording import Recording
from src.ofdm.modulate import modulate_sequence
from src.coding.encode import encode_bit_string
from src.coding.decode import decode_symbol_sequence
from src.coding.utils import text_to_bin
from src.plotting.plot_recording import plot_recording
from config import OUTPUT_DIR, SAMPLING_FREQ
import os


def run():
    """main loop"""
    # file_name_short = input("File name to save (.wav): ")
    # file_name_full = os.path.join(OUTPUT_DIR, file_name_short + ".wav")

    # dummy data
    #data = text_to_bin("Wapiti")
    data = format(1530, '016b')
    print(data)
    # making a long data file
    for i in range(10):
        data += data
    print("data fully created")
    # doing the encoding and modulation
    QPSK = encode_bit_string(data)
    print(QPSK)
    print("data encoded into QPSK")
    modulated_data = modulate_sequence(QPSK, N=1024, K=1000)
    print("QPSK data modulated; ready for playback")
    # now make the recording and play/display, can probably save this as wav, or slot it between chirps
    wav = Recording.from_list(modulated_data, SAMPLING_FREQ)
    wav.play()
    plot_recording(wav)


if __name__ == "__main__":
    print("\nTeam Wapiti - Creating Data\n~~~~~~~~~~~~~~~~~~~\n")
    run()
