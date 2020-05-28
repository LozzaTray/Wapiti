"""Code for recording and playing back audio"""
from src.audio.recording import Recording
from src.plotting.plot_recording import plot_correlation
from src.file_io.utils import get_output_file_path
from config import N, K, C, D, W, Q, q, F, F0, F1
from src.audio.chirp import generate_chirp_recording
import matplotlib.pyplot as plt
import numpy as np


def run():
    """main loop"""
    P = N + K
    WP = W * P
    samples_threshold = 0.05
    magnitude_threshold = 0.8
    
    signal_file = 'elk-wrong' #input("Signal to load (.wav): ")
    signal_file = get_output_file_path(signal_file + ".wav")
    signal = Recording.from_file(signal_file)

    reference_file = 'c' #input("Reference signal (.wav): ")
    reference_file = get_output_file_path(reference_file + ".wav")
    reference = Recording.from_file(reference_file)

    c = signal.correlate(reference)
    plt.plot(c)
    
    signalList = signal.get_frames_as_int16() 

    i = 0
    data = []

    while True:
        c_trunc = c[i:i+WP] #obtain a truncated peak
        print(i, i+WP)
         
        #find index and value of maximum value of correlation output
        peak_index_t = np.argmax(c_trunc)
        peak_value = c_trunc[peak_index_t]
        peak_index = i + peak_index_t
        
        print("PEAK:", peak_index)
        
        
        #if there are not enough samples for another transmission, end the process
        if len(c) < int(i+WP+225*P*(1-samples_threshold)):
            break
        
        #if there is not another peak of similar magnitude after 220P±1% samples, end the process
        next_peak_range = c[int(i+WP+220*P*(1-samples_threshold)):int(i+WP+220*P*(1+samples_threshold))]
        if np.max(c[peak_index:peak_index+len(next_peak_range)]) < peak_value*magnitude_threshold:
            break
        
        data.append(signalList[peak_index:peak_index+220*P]) #append list of data values between chirp
        i+=int(220*P*(1-samples_threshold)) #increase index by 220P-1% samples from previous peak
        
    print("DATA SEQUENCES FOUND:", len(data))


if __name__ == "__main__":
    print("\nTeam Wapiti - Extract Data sequence\n~~~~~~~~~~~~~~~~~~~\n")
    run()
