"""code to generate artificial recording for transmitting known data"""
from src.audio.recording import Recording
from src.ofdm.modulate import modulate_sequence
from src.coding.encode import encode_bit_string
from src.coding.decode import decode_symbol_sequence
from src.coding.utils import text_to_bin
from src.plotting.plot_recording import plot_recording
from config import OUTPUT_DIR, F
import wave
import os


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
    final_data = scaling * modulated_data
    # now make the recording and play/display, can probably save this as wav, or slot it between chirps
    wav = Recording.from_list(final_data, F)
    wav.play()
    plot_recording(wav)
    save = input("would you like to save this recording? (y/n)")
    if save == "y": wav.save(os.path.join(OUTPUT_DIR, input("please enter a file name ") + ".wav"))
    else: print("file discarded, lost to the abyss")




if __name__ == "__main__":
    print("\nTeam Wapiti - Creating Data\n~~~~~~~~~~~~~~~~~~~\n")
    run()
