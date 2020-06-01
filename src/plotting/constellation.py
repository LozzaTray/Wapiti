"""Module for plotting complex constellation"""
import matplotlib.pyplot as plt
import numpy as np


def plot_complex_symbols(symbol_sequence):
    """Plots symbols on complex plane"""
    real = np.real(symbol_sequence)
    imag = np.imag(symbol_sequence)

    plt.figure()
    plt.scatter(real, imag)
    plt.show()