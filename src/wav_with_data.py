"""code to generate artificial recording for transmitting known data"""
from src.audio.recording import Recording
from src.ofdm.modulate import modulate_sequence
from src.coding.encode import encode_bit_string
from src.coding.decode import decode_symbol_sequence
from config import OUTPUT_DIR
import os


def run():
    """main loop"""
    # file_name_short = input("File name to save (.wav): ")
    # file_name_full = os.path.join(OUTPUT_DIR, file_name_short + ".wav")

    # setting the sampling frequency we want
    samp_freq = 48000
    # dummy data
    data = b'0000010111111010'
    # making a long data file
    for i in range(14):
        data += data
    # doing the encoding and modulation
    print("data fully created")
    QPSK = encode_bit_string(data)
    print("data encoded into QPSK")
    modulated_data = modulate_sequence(QPSK)
    print("QPSK data modulated; ready for playback")
    # now make the recording and play/display, can probably save this as wav, or slot it between chirps
    recording = Recording.from_list(modulated_data,samp_freq)
    recording.play()
    recording.display()


if __name__ == "__main__":
    print("\nTeam Wapiti - Creating Data\n~~~~~~~~~~~~~~~~~~~\n")
    run()
