import numpy as np


def scale_to_int16(x_arr):
    """Takes a sequence shifts it to zero mean and scales it to int16"""
    x_arr = np.array(x_arr)
    
    mean = np.mean(x_arr)
    zero_mean_arr = x_arr - mean

    max_abs = np.max(np.abs(x_arr))
    scaling = (2**15 - 1) / max_abs
    scaled_arr = zero_mean_arr * scaling

    return scaled_arr.astype(np.int16)