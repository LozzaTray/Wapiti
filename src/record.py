"""Code for recording and playing back audio"""
from audio.audio import record, playback
from file_io.output import display_recording
from config import OUTPUT_DIR
import os

def run():
    """main loop"""
    file_name_short = input("File name to save (.wav): ")
    file_name_full = os.path.join(OUTPUT_DIR, file_name_short + ".wav")

    duration = int(input("Duration of recording (seconds): "))
    channel_num = int(input("Number of channels to use (1 or 2): "))

    recording = record(duration, file_name_full, channels = channel_num)
    #display_recording(recording)
    playback(file_name_full)



if __name__ == "__main__":
    print("\nTeam Wapiti - Record\n~~~~~~~~~~~~~~~~~~~\n")
    run()