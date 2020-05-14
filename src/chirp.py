"""Code for recording and playing back audio"""
from src.audio.recording import Recording
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
import pyaudio

def run():
    
    t1 = 5
    f0 = 400
    f1 = 10000
    fs = 192000
    t = np.linspace(0, t1, fs*t1)
    data = scipy.signal.chirp(t, f0, t1, f1, method='linear', phi=0, vertex_zero=True).astype(np.float16)
    #print(data)
    #plt.plot(data)
    
    recording = Recording.from_list(data, fs)
    recording.play()
    


if __name__ == "__main__":
    print("\nTeam Wapiti - Open Recording\n~~~~~~~~~~~~~~~~~~~\n")
    run()
