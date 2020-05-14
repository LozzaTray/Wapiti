"""Code for recording and playing back audio"""
from src.audio.recording import Recording
from config import OUTPUT_DIR
import os


def run():
    """main loop"""
    signal_file = input("Signal to load (.wav): ")
    signal_file = os.path.join(OUTPUT_DIR, signal_file + ".wav")

    signal = Recording.from_file(signal_file)

    reference_file = input("Refernce signal (.wav): ")
    reference_file = os.path.join(OUTPUT_DIR, reference_file + ".wav")

    reference = Recording.from_file(reference_file)
    

    signal.correlate(reference)


if __name__ == "__main__":
    print("\nTeam Wapiti - Correlate\n~~~~~~~~~~~~~~~~~~~\n")
    run()
