import numpy as np


def gen_time_array(num_samples: int, rate: int):
    """generates time array"""
    time = np.linspace(0, num_samples / rate, num=num_samples)
    return time