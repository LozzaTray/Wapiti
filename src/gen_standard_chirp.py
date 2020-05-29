"""Code for recording and playing back audio"""
from src.audio.chirp import generate_chirp_recording
from src.plotting.plot_recording import plot_recording
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
import os
import pyaudio
from config import F, F0, F1, C, N, _K_dict
from src.file_io.utils import get_recording_file_path


def run():
    mode = input("Which mode {A, B, C}: ")
    K = _K_dict[mode]
    P = N + K

    print("Generating chirp...")
    chirp = generate_chirp_recording(F, F0, F1, C * P)

    file_name_short = "chirp-" + mode
    file_name_full = get_recording_file_path(file_name_short + ".wav")

    print("Saving under " + file_name_short)
    chirp.save(file_name_full)
    plot_recording(chirp)
    


if __name__ == "__main__":
    print("\nTeam Wapiti - Gen Standard Chirp\n~~~~~~~~~~~~~~~~~~~\n")
    run()
