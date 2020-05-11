from packages.ofdm import demodulate


def test_demodulate():
    N = 6
    K = 2

    received_sequence = [1, 1, 1, 1, 1, 1, 1, 1]
    channel_response = [1]
    demodulated_sequence = demodulate(received_sequence, channel_response, N=N, K=K)
    assert len(demodulated_sequence) == N/2 - 1