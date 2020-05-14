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

    # setting the data values we want to transmit
    data = b'0000010111111010'
    QPSK = encode_bit_string(data)
    print(data)
    print("\n")
    print(QPSK)
    print("\n")
    print(decode_symbol_sequence(QPSK))
    print("\n")
    modulated_data = modulate_sequence(QPSK)
    print(modulated_data)
    print("\n")

    # recording.display()
    # recording.save(file_name_full)


if __name__ == "__main__":
    print("\nTeam Wapiti - Creating Data\n~~~~~~~~~~~~~~~~~~~\n")
    run()
