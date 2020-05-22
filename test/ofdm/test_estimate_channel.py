from src.audio.recording import Recording
from src.ofdm.estimate_channel import estimate_channel
import numpy as np


def test_estimate_channel_simple():
    rate = 1
    signal = [2, 3, 1, 2, 3]
    filt = [1, 0, 0]
    N = 3
    K = 2

    signal_rec = Recording.from_list(signal, rate)

    sim_signal_rec = signal_rec.pass_through_channel(filt)
    sim_signal = sim_signal_rec.get_frames_as_int16()[0 : N+K]

    h = estimate_channel(sim_signal, signal, N=N, K=K)
    assert np.allclose(h, filt) == True


def test_estimate_channel_average():
    rate = 1
    signal = [2, 3, 1, 2, 3, 2, 3, 1, 2, 3]
    filt = [1, 0, 0]
    N = 3
    K = 2

    signal_rec = Recording.from_list(signal, rate)

    sim_signal_rec = signal_rec.pass_through_channel(filt)
    sim_signal = sim_signal_rec.get_frames_as_int16()[0: (N+K) * 2]

    h = estimate_channel(sim_signal, signal, N=N, K=K)
    assert np.allclose(h, filt) == True


def test_estimate_channel_hard():
    rate = 1
    signal = [2, 3, 1, 2, 3, 2, 3, 1, 2, 3]
    filt = [10, 2, 1]
    N = 3
    K = 2

    signal_rec = Recording.from_list(signal, rate)

    sim_signal_rec = signal_rec.pass_through_channel(filt)
    sim_signal = sim_signal_rec.get_frames_as_int16()[0: (N+K) * 2]

    h = estimate_channel(sim_signal, signal, N=N, K=K)
    assert np.allclose(h, filt) == True