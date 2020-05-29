from src.ofdm.modulate import modulate_sequence
from src.ofdm.demodulate import demodulate_sequence
import numpy as np


def test_recovery_ideal_channel():
    N = 8
    K = 2
    Q1 = 1
    Q2 = 3
    P = N + K

    channel_response = [1]

    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    modulated_sequence = modulate_sequence(data, N, K, Q1, Q2)

    sent_sequence = np.convolve(modulated_sequence, channel_response)[0 : P]
    demodulated_sequence = demodulate_sequence(sent_sequence, channel_response, N, K, Q1, Q2)
    just_real_integers = np.round(np.real_if_close(demodulated_sequence))

    assert list(just_real_integers) == list(data)


def test_recovery_real_channel():
    N = 8
    K = 2
    Q1 = 1
    Q2 = 3
    P = N + K

    channel_response = [1, 2]

    actual_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    modulated_sequence = modulate_sequence(actual_data, N, K, Q1, Q2)

    sent_sequence = np.convolve(modulated_sequence, channel_response)[0 : P]
    demodulated_sequence = demodulate_sequence(sent_sequence, channel_response, N, K, Q1, Q2)
    just_real_integers = np.round(np.real_if_close(demodulated_sequence))

    data_length = len(actual_data)
    received_data = just_real_integers[:data_length]

    assert list(received_data) == list(actual_data)