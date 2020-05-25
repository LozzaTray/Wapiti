from src.ofdm.utils import dft, idft
import numpy as np


def calc_abs_angle_error(h, N):
    """Given a channel response, calculate the phase"""
    H_arr = dft(h, N)
    phase = np.unwrap(np.angle(H_arr))
    mean_squared_phase = np.mean(phase ** 2)
    return mean_squared_phase
    

def estimate_channel(y_arr, x_arr, N: int, K: int):
    """
    Estimates the channel
    y_arr: array of received ofdm seq (post-channel)
    x_arr: array of sent ofdm seq (pre-channel)
    N: dft block size
    K: cyclic prefix size

    Returns:
    h: arr[num] the time domain response concatenated to K = 1
    """
    data_length = len(y_arr)

    if (data_length != len(x_arr)):
        raise ValueError("Length of y and x arrays must match")

    if(data_length % (N+K) != 0):
        raise ValueError("Supplied arrays are not divisible by the block length")

    H = []
    num_blocks = int(data_length / (N + K))

    for i in range(0, num_blocks):
        lower_index = i*(N+K) + K # hacky soln
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

        # set equal to neighbours
        H_sample[0] = H_sample[1]
        H_sample[N//2] = H_sample[N//2 + 1]

        H.append(H_sample)

    # take average
    H = np.average(H, axis=0)
    h = idft(H, N)
    #h = np.real_if_close(h) # must be real channel in reality
    return h