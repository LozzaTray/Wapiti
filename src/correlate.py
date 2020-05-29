"""Code for recording and playing back audio"""
from src.audio.recording import Recording
from src.plotting.plot_recording import plot_correlation
from src.file_io.utils import get_recording_file_path


def run():
    """main loop"""
    signal_file = input("Signal to load (.wav): ")
    signal_file = get_recording_file_path(signal_file + ".wav")
    signal = Recording.from_file(signal_file)

    reference_file = input("Reference signal (.wav): ")
    reference_file = get_recording_file_path(reference_file + ".wav")
    reference = Recording.from_file(reference_file)

    plot_correlation(signal, reference)


if __name__ == "__main__":
    print("\nTeam Wapiti - Correlate\n~~~~~~~~~~~~~~~~~~~\n")
    run()
