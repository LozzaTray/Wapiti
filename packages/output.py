"""Module for saving data"""
import numpy


def write_binary(filename, data_array):
    numpy.savetxt(filename, data_array, fmt="%d", newline="")


def write_bytes(filename, data_array):
    num_bytes = int(len(data_array) / 8)
    byte_array = numpy.reshape(data_array, (8, num_bytes))
    numpy.savetxt(filename, byte_array, fmt="%d")    


def write_rows(filename, data_array):
    numpy.savetxt(filename, data_array, fmt="%s")
