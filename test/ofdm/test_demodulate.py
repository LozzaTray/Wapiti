from src.ofdm.demodulate import demodulate_sequence

def test_demodulate_sequence():
    N = 6
    K = 2

    received_sequence = [1, 1, 1, 1, 1, 1, 1, 1]
    channel_response = [1]
    demodulated_sequence = demodulate_sequence(received_sequence, channel_response, N=N, K=K)
    assert len(demodulated_sequence) == N/2 - 1