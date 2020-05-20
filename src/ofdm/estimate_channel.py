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

        Y_freq_arr = dft(y_block, N)
        X_freq_arr = dft(x_block, N)

        H_sample = np.true_divide(
            Y_freq_arr, 
            X_freq_arr,
            out=np.zeros_like(Y_freq_arr),
            where=X_freq_arr!=0
        )
        H.append(H_sample)

    # take average
    H = np.average(H, axis=0)
    return H


def plot_H_in_time(H_arr, N):
    h = idft(H_arr, N)
    plt.figure()
    plt.title("Time Response")
    magnitude = abs(h)
    plt.plot(magnitude)
    plt.show()


def plot_H_freq_domain(H_arr):
    fig, (ax1, ax2) = plt.subplots(2, sharex=True)
    fig.suptitle("Frequency plots")

    ax1.plot(abs(H_arr))
    ax1.set(ylabel="Gain")

    phase = np.unwrap(np.angle(H_arr, deg=True))
    ax2.plot(phase)
    ax2.set(ylabel="Phase (degrees)", xlabel="Frequency bin")

    plt.show()

