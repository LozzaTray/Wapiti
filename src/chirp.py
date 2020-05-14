"""Code for recording and playing back audio"""
from src.audio.recording import Recording
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
import pyaudio

def run():
    fs = 48000
    T = 1
    t = np.linspace(0, T, int(T * fs))
    f0 = 20
    f1 = 2000
    t1 = T
    data = (scipy.signal.chirp(t, f0, t1, f1, method='linear', phi=0, vertex_zero=True)*(2**15 - 1)).astype(np.int16)
    print(data)
    
    #plt.figure(1)
    #plt.plot(data)
    #plt.show
    
    recording = Recording.from_list(data, fs)
    recording.play()
    recording.display()
    


if __name__ == "__main__":
    print("\nTeam Wapiti - Open Recording\n~~~~~~~~~~~~~~~~~~~\n")
    run()
