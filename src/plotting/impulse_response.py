"""Module for plotting all things channel response"""
import matplotlib.pyplot as plt
from src.ofdm.utils import dft
from src.plotting.utils import gen_time_array
import numpy as np

def plot_h_in_time(h_arr):
    plt.figure()
    h_real = np.real(h_arr)
    plt.title("Time Response of Filter")
    plt.plot(h_real)
    plt.ylabel("h coefficient")
    plt.xlabel("Sample index")
    plt.show()


def plot_h_freq_domain(h_arr, N):
    H_arr = dft(h_arr, N)
    fig, (ax1, ax2) = plt.subplots(2, sharex=True)
    fig.suptitle("Frequency Response of Filter")

    magnitude = np.abs(H_arr)
    ax1.plot(magnitude)
    ax1.set(ylabel="Gain")

    phase = np.unwrap(np.angle(H_arr, deg=True))
    ax2.plot(phase)
    ax2.set(ylabel="Phase (degrees)", xlabel="Frequency bin")

    plt.show()