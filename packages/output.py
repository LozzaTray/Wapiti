"""Module for saving data"""
import numpy


def write_binary(filename, data_array):
    numpy.savetxt(filename, data_array, fmt="%d", newline="")


def write_csv(filename, data_array):
    numpy.savetxt(filename, data_array, fmt="%d", newline=",")
