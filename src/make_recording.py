"""Code for recording and playing back audio"""
from src.audio.recording import Recording
from src.plotting.plot_recording import plot_recording
from src.file_io.utils import get_recording_file_path
import os


def run():
    """main loop"""
    file_name_short = input("File name to save (.wav): ")
    file_name_full = get_recording_file_path(file_name_short + ".wav")

    duration = int(input("Duration of recording (seconds): "))

    recording = Recording.from_mic(duration=duration)
    recording.save(file_name_full)
    
    plot_recording(recording)


if __name__ == "__main__":
    print("\nTeam Wapiti - Record\n~~~~~~~~~~~~~~~~~~~\n")
    run()
