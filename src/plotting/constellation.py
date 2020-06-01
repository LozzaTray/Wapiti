"""Module for plotting complex constellation"""
import matplotlib.pyplot as plt
import numpy as np


def plot_complex_symbols(symbol_sequence):
    """Plots symbols on complex plane"""
    real = np.real(symbol_sequence)
    imag = np.imag(symbol_sequence)

    num_points = len(symbol_sequence)
    num_blocks = 6
    block_size = num_points //  num_blocks


    plt.figure()
    for i in range(0, num_blocks):
        plt.scatter(
            real[i*block_size : (i+1) * block_size], 
            imag[i*block_size : (i+1) * block_size], 
            s=0.1,
            label=str(i)
        )
    plt.grid()
    plt.legend()
    plt.show()