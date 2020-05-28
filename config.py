import os

_curr_dir = os.path.dirname(__file__)
DATA_DIR = os.path.join(_curr_dir, "data")
OUTPUT_DIR = os.path.join(_curr_dir, "output")

MODE = "B" # "A", "B" or "C"
_K_dict = {"A": 224, "B": 704, "C": 1184}

# OFDM params
F = 48000
N = 4096
K = _K_dict[MODE]
Q = 2047
q = 2

# Frame params
F0 = 2000
F1 = 4000
C = 5
D = 20
W = 180