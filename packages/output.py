"""Module for saving data"""
import numpy


def write_to_file(filename, data_array):
    numpy.savetxt(filename, data_array, delimiter=",")