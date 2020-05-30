from src.ofdm.modulate import modulate_sequence
from src.ofdm.demodulate import demodulate_sequence
import numpy as np


def test_recovery_ideal_channel():
    N = 8
    K = 2
    Q1 = 1
    Q2 = 3

    Q = Q2 - Q1
    P = N + K

    channel_response = [1]

    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    num_packets = len(data) // Q

    modulated_sequence = modulate_sequence(data, N, K, Q1, Q2)

    assert len(modulated_sequence) == num_packets * P

    sent_sequence = np.convolve(modulated_sequence, channel_response)[0 : num_packets * P]
    demodulated_sequence = demodulate_sequence(sent_sequence, channel_response, channel_response, N, K, Q1, Q2)
    just_real_integers = np.round(np.real_if_close(demodulated_sequence))

    assert list(just_real_integers) == list(data)


def test_recovery_real_channel():
    N = 8
    K = 2
    Q1 = 1
    Q2 = 3

    Q = Q2 - Q1
    P = N + K

    channel_response = [2, 1]

    actual_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    num_packets = len(actual_data) // Q

    modulated_sequence = modulate_sequence(actual_data, N, K, Q1, Q2)

    sent_sequence = np.convolve(modulated_sequence, channel_response)[0 : num_packets * P]
    demodulated_sequence = demodulate_sequence(sent_sequence, channel_response, channel_response, N, K, Q1, Q2)
    received_data = np.round(np.real_if_close(demodulated_sequence))

    assert list(received_data) == list(actual_data)