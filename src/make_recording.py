"""Code for recording and playing back audio"""
from src.audio.recording import Recording
from src.plotting.plot_recording import plot_recording
from config import OUTPUT_DIR
import os


def run():
    """main loop"""
    file_name_short = input("File name to save (.wav): ")
    file_name_full = os.path.join(OUTPUT_DIR, file_name_short + ".wav")

    duration = int(input("Duration of recording (seconds): "))

    recording = Recording.from_mic(duration=duration)
    recording.play()
    recording.save(file_name_full)
    
    plot_recording(recording)


if __name__ == "__main__":
    print("\nTeam Wapiti - Record\n~~~~~~~~~~~~~~~~~~~\n")
    run()
