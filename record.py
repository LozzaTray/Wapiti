"""Code for decoding data"""
from packages.audio import record
from packages.audio import playback
import os

curr_dir = os.path.dirname(__file__)


def run():
    """main loop"""
    file_name_short = input("File name to save (.wav): ")
    file_name_full = os.path.join(curr_dir, "data/" + file_name_short + ".wav")

    duration = int(input("Duration of recording (seconds): "))

    channel_num = int(input("Number of channels to use (1 or 2): "))
    
    record(duration, file_name_full, channels = channel_num)
    
    playback (file_name_full)



if __name__ == "__main__":
    print("\nTeam Wapiti - Record\n~~~~~~~~~~~~~~~~~~~\n")
    run()