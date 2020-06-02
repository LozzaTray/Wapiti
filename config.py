import os

_curr_dir = os.path.dirname(__file__)
DATA_DIR = os.path.join(_curr_dir, "data")
OUTPUT_DIR = os.path.join(_curr_dir, "output")
RECORDING_DIR = os.path.join(_curr_dir, "recordings")

_K_dict = {"A": 224, "B": 704, "C": 1184}
_Q_dict = {"1": (1, 2048), "2": (100, 1500), "3": (100, 1000), "4": (101, 1501)}

# OFDM params
F = 48000
N = 4096
q = 2

# Frame params
F0 = 0
F1 = 8000
C = 5
D = 20
W = 180


def get_K(mode):
    if mode in _K_dict.keys():
        return _K_dict[mode]
    else:
        raise ValueError("Invalid mode")

def get_Q(mode):
    if mode in _Q_dict.keys():
        return _Q_dict[mode]
    else:
        raise ValueError("Invalid mode")