"""Module for saving data"""
import numpy


def write_binary(filename, data_array):
    numpy.savetxt(filename, data_array, fmt="%d", newline="")


def write_rows(filename, data_array):
    numpy.savetxt(filename, data_array, fmt="%s")
