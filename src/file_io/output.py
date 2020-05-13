"""Module for saving data"""
import numpy
import matplotlib.pyplot as plt


def write_binary(filename, data_array):
    numpy.savetxt(filename, data_array, fmt="%d", newline="")


def write_bytes(filename, data_array):
    num_bytes = int(len(data_array) / 8)
    byte_array = numpy.reshape(data_array, (8, num_bytes))
    numpy.savetxt(filename, byte_array, fmt="%d")    


def write_rows(filename, data_array):
    numpy.savetxt(filename, data_array, fmt="%s")


def display_recording(data_array):
    """Displays recorded audio"""
    plt.figure()
    plt.plot(data_array)
    plt.xlabel("sample index")
    plt.ylabel("amplitude")
    #plt.savefig('plot.png', dpi=100)
    plt.show()
