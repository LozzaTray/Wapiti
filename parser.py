"""Module for parsing of data files"""
from numpy import genfromtxt


def read_csv_as_array(filepath):
    """Reads csv and returns contents as numpy array"""
    data_array = genfromtxt(filepath, delimiter=",")
    return data_array