"""code to generate artificial recording for transmitting known data"""
from src.audio.recording import Recording
from src.ofdm.modulate import modulate_block
from config import OUTPUT_DIR
import os


def run():
    """main loop"""
    # file_name_short = input("File name to save (.wav): ")
    # file_name_full = os.path.join(OUTPUT_DIR, file_name_short + ".wav")

    # setting the data values we want to transmit
    binary_data = [0, 0b00, 1, 0b01, 3, 0b11, 2, 0b10]
    QPSK_data = []
    print(binary_data)
    print("\n")
    for i in range(len(binary_data)):
        d = binary_data[i]
        if d == 0: QPSK_data.append(complex(1, 1))
        if d == 1: QPSK_data.append(complex(-1, 1))
        if d == 2: QPSK_data.append(complex(1, -1))
        if d == 3: QPSK_data.append(complex(-1, -1))
    print(QPSK_data)
    print("\n")
    modulated_data = modulate_block(binary_data,len(binary_data)/2,10)
    print(modulated_data)
    print("\n")

    # recording.display()
    # recording.save(file_name_full)


if __name__ == "__main__":
    print("\nTeam Wapiti - Creating Data\n~~~~~~~~~~~~~~~~~~~\n")
    run()
