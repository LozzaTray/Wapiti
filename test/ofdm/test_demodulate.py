from src.ofdm.demodulate import demodulate_sequence

def test_demodulate_sequence():
    N = 6
    K = 2
    Q1 = 1
    Q2 = 5
    Q = Q2 - Q1 # 4

    received_sequence = [1, 1, 1, 1, 1, 1, 1, 1]
    channel_response = [1]
    demodulated_sequence = demodulate_sequence(received_sequence, channel_response, N, K, Q1, Q2)
    assert len(demodulated_sequence) == Q