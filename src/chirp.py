"""Code for recording and playing back audio"""
from src.audio.recording import Recording
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt

def run():
    fs = 96000
    t = np.linspace(0, 1, fs)
    f0 = 400
    f1 = 1000
    t1 = 1
    data = scipy.signal.chirp(t, f0, t1, f1, method='linear', phi=0, vertex_zero=True)*30000
    print(data)
    plt.plot(data[-100:])
    
    recording = Recording.from_list(data, fs)
    recording.play()
    


if __name__ == "__main__":
    print("\nTeam Wapiti - Open Recording\n~~~~~~~~~~~~~~~~~~~\n")
    run()
