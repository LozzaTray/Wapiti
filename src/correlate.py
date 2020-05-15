"""Code for recording and playing back audio"""
from src.audio.recording import Recording
from src.plotting.plot_recording import plot_correlation
from config import OUTPUT_DIR
import os


def run():
    """main loop"""
    #signal_file = input("Signal to load (.wav): ")
    signal_file = "received_chirps"
    signal_file = os.path.join(OUTPUT_DIR, signal_file + ".wav")

    signal = Recording.from_file(signal_file)

    #reference_file = input("Reference signal (.wav): ")
    reference_file = "chirp"
    reference_file = os.path.join(OUTPUT_DIR, reference_file + ".wav")

    reference = Recording.from_file(reference_file)
    plot_correlation(signal, reference)


if __name__ == "__main__":
    print("\nTeam Wapiti - Correlate\n~~~~~~~~~~~~~~~~~~~\n")
    run()
