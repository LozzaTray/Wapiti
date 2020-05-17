"""Code for recording and playing back audio"""
from src.audio.recording import Recording
from src.plotting.plot_recording import plot_recording
from config import OUTPUT_DIR
import os


def run():
    """main loop"""
    file_name_short = input("File name to open (.wav): ")
    file_name_full = os.path.join(OUTPUT_DIR, file_name_short + ".wav")

    rec = Recording.from_file(file_name_full)
    rec.play()
    plot_recording(rec)


if __name__ == "__main__":
    print("\nTeam Wapiti - Open Recording\n~~~~~~~~~~~~~~~~~~~\n")
    run()
