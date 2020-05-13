from src.ofdm.modulate import modulate_sequence


def test_modulate_sequence():
    K = 2
    N = 4
    M = int(N/2) - 1 # number of useful symbols in each block
    P = N + K # size of each ofdm block
    x = [1, 2, 3, 4, 5, 6]
    y = modulate_sequence(x, N, K)
    assert len(y) == P * len(x) / M