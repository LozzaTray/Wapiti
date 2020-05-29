"""Code for recording and playing back audio"""
from src.audio.recording import Recording
from src.plotting.plot_recording import plot_recording
from src.file_io.utils import get_recording_file_path


def run():
    """main loop"""
    file_name_short = input("File name to open (.wav): ")
    file_name_full = get_recording_file_path(file_name_short + ".wav")

    rec = Recording.from_file(file_name_full)
    plot_recording(rec)


if __name__ == "__main__":
    print("\nTeam Wapiti - Open Recording\n~~~~~~~~~~~~~~~~~~~\n")
    run()
