"""Code for recording and playing back audio"""
from src.audio.recording import Recording
from src.audio.chirp import generate_chirp_array_as_int16
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
import pyaudio

def run():
    fs = 48000
    T = 1
    f0 = 20
    f1 = 1000

    data = generate_chirp_array_as_int16(
        duration=T,
        sampling_freq=fs,
         f0=f0,
         f1=f1
    )
    
    recording = Recording.from_list(data, fs)
    recording.play()
    recording.display()
    


if __name__ == "__main__":
    print("\nTeam Wapiti - Play Chirp\n~~~~~~~~~~~~~~~~~~~\n")
    run()
