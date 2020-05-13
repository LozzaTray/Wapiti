"""code for doing the channel analysis"""
import os
from modulation.fourier import dft
from audio.audio import record, playback
from file_io.wav import read_wav
import wave
from config import OUTPUT_DIR


def run():
    """main loop"""
    file_name_short = input("File name to save (.wav): ")
    file_name_full = os.path.join(OUTPUT_DIR, file_name_short + ".wav")

    duration = int(input("Duration of recording (seconds): "))
    channel_num = int(input("Number of channels to use (1 or 2): "))

    print("Recording...")
    record(duration, file_name_full, channels=channel_num)
    print("Done")

    #print("Playing back")      #not necessary right now
    #playback(file_name_full)   #add in later if we want
    file_info = read_wav(file_name_full)
    print(file_info[1:4])



if __name__ == "__main__":
    print("\nTeam Wapiti - Record\n~~~~~~~~~~~~~~~~~~~\n")
    run()