import os

_curr_dir = os.path.dirname(__file__)
DATA_DIR = os.path.join(_curr_dir, "data")
OUTPUT_DIR = os.path.join(_curr_dir, "output")
RECORDING_DIR = os.path.join(_curr_dir, "recordings")

MODE = "C" # "A", "B" or "C"
_K_dict = {"A": 224, "B": 704, "C": 1184}

# OFDM params
F = 48000
N = 4096
K = _K_dict[MODE]
Q1 = 100
Q2 = 1500
Q = Q2 - Q1
q = 2

# Frame params
F0 = 2000
F1 = 4000
C = 5
D = 20
W = 180