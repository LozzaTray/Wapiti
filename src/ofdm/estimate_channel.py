from src.ofdm.utils import dft, idft
import matplotlib.pyplot as plt
import numpy as np


def estimate_channel(y_arr, x_arr, N: int, K: int):
    """Estimates the channel"""
    data_length = len(y_arr)

    if (data_length != len(x_arr)):
        raise ValueError("Length of y and x arrays must match")

    if(data_length % (N+K) != 0):
        raise ValueError("Supplied arrays are not divisible by the block length")

    H = []
    num_blocks = int(data_length / (N + K))

    for i in range(0, num_blocks):
        lower_index = i*(N+K) + K
        upper_index = lower_index + N

        y_block = y_arr[lower_index : upper_index]
        x_block = x_arr[lower_index : upper_index]

        Y_freq_arr = dft(y_arr, N)
        X_freq_arr = dft(x_arr, N)

        H_sample = np.divide(Y_freq_arr, X_freq_arr)
        H.append(H_sample)

    return H


def plot_H_in_time(H_arr, N):
    H_arr[0] = 0
    H_arr[512] = 0
    h = idft(H_arr, N)
    plt.figure()
    magnitude = abs(h)
    phase = np.angle(h)
    plt.plot(magnitude)
    plt.show()
