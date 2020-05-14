from src.ofdm.modulate import modulate_sequence
from src.ofdm.demodulate import demodulate_sequence
import numpy as np


def test_recovery_ideal_channel():
    N = 6
    K = 2
    channel_response = [1]

    data = [1, 2, 3, 4, 5, 6, 7, 8]

    modulated_sequence = modulate_sequence(data, N, K)

    sent_sequence = np.convolve(modulated_sequence, channel_response)
    demodulated_sequence = demodulate_sequence(sent_sequence, channel_response, N=N, K=K)
    just_real_integers = np.round(np.real_if_close(demodulated_sequence))

    assert list(just_real_integers) == list(data)


def test_recovery_real_channel():
    N = 6
    K = 3
    channel_response = [1, 2]

    data = [1, 2, 3, 4, 5, 6, 7, 8]

    modulated_sequence = modulate_sequence(data, N, K)

    sent_sequence = np.convolve(modulated_sequence, channel_response)
    demodulated_sequence = demodulate_sequence(sent_sequence, channel_response, N=N, K=K)
    just_real_integers = np.round(np.real_if_close(demodulated_sequence))

    assert list(just_real_integers) == list(data)