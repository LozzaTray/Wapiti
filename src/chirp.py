"""Code for recording and playing back audio"""
from src.audio.recording import Recording
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
import pyaudio

def run():
    
#    p = pyaudio.PyAudio()
#
#    volume = 0.5     # range [0.0, 1.0]
#    fs = 48000       # sampling rate, Hz, must be integer
#    duration = 1.0   # in seconds, may be float
#    f = 10000.0        # sine frequency, Hz, may be float
#    
#    # generate samples, note conversion to float32 array
#    samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
#    
#    # for paFloat32 sample values must be in range [-1.0, 1.0]
#    stream = p.open(format=pyaudio.paFloat32,
#                    channels=1,
#                    rate=fs,
#                    output=True)
#    
#    # play. May repeat with different volume values (if done interactively) 
#    stream.write(volume*samples)
#    
#    stream.stop_stream()
#    stream.close()
#
#    p.terminate()
    
    t1 = 5
    f0 = 400
    f1 = 10000
    fs = 48000
    t = np.linspace(0, t1, fs*t1)
    data = (scipy.signal.chirp(t, f0, t1, f1, method='linear', phi=0, vertex_zero=True)*0.1).astype(np.float16)
    print(data)
    plt.plot(data[-100:])
    
    recording = Recording.from_list(data, fs)
    recording.play()
    


if __name__ == "__main__":
    print("\nTeam Wapiti - Open Recording\n~~~~~~~~~~~~~~~~~~~\n")
    run()
