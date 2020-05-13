from src.modulation.ofdm import demodulate_sequence, insert_cyclic_prefix, modulate_sequence


def test_demodulate():
    N = 6
    K = 2

    received_sequence = [1, 1, 1, 1, 1, 1, 1, 1]
    channel_response = [1]
    demodulated_sequence = demodulate_sequence(received_sequence, channel_response, N=N, K=K)
    assert len(demodulated_sequence) == N/2 - 1


def test_insert_cyclic_prefix():
    K = 2
    x = [1, 2, 3]
    y = insert_cyclic_prefix(x, K)
    assert list(y) == list([2, 3, 1, 2, 3])


def test_modulate():
    K = 2
    N = 4
    M = int(N/2) - 1 # number of useful symbols in each block
    P = N + K # size of each ofdm block
    x = [1, 2, 3, 4, 5, 6]
    y = modulate_sequence(x, N, K)
    assert len(y) == P * len(x) / M