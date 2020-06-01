"""Module for performing ofdm tasks"""
from src.ofdm.utils import dft, pad_so_divisible
import numpy as np
import cmath


def phase_correct(symbol_sequence, phase_gradient):
    """Correct phase"""
    corrected_sequence = np.zeros_like(symbol_sequence)
    num_symbols = len(symbol_sequence)

    for i in range(0, num_symbols):
        corrected_sequence[i] = symbol_sequence[i] * cmath.rect(1, - i * phase_gradient / num_symbols)
    
    return corrected_sequence


def gen_H_estimate(mag_start, mag_end, phase_start, phase_end, step, num_steps):
    """linearly interpolate response"""
    mag = mag_start + (mag_end - mag_start) * step / num_steps
    phase = phase_start + (phase_end - phase_start) * step / num_steps
    nprect = np.vectorize(cmath.rect)
    return nprect(mag, phase)


def demodulate_block(block, H_arr, N, K, Q1, Q2, phase_gradient):
    """
    demodulates a single block
        block: complex[] length N+K
        H_arr: complex[] length N
    """
    
    if len(H_arr) != N:
        raise ValueError("Channel response length does not match N")

    if (len(block) != N + K):
        raise ValueError("Block length does not match N + K")

    # discard cyclic prefix
    sliced_block = block[K:]

    # take dft of block without cyclic pref
    dfted_block = dft(sliced_block, N)
    demodulated_block = np.divide(dfted_block, H_arr)

    # only take positive frequency bins
    relevant_bins = demodulated_block[Q1: Q2]
    corrected_bins = phase_correct(relevant_bins, phase_gradient)
    return corrected_bins


def demodulate_sequence(received_sequence, channel_impulse_response_start, channel_impulse_response_end, N, K, Q1, Q2):
    """decodes by taking the DFT of the received_sequence and channel_impulse_response
    then apply point-wise division to get the true symbol value"""

    if (N % 2 != 0):
        raise ValueError("N must be an even integer")

    H_start = dft(channel_impulse_response_start, N)
    H_end = dft(channel_impulse_response_end, N)

    # phase
    x = list(range(Q1, Q2))
    phase_start = np.unwrap(np.angle(H_start))
    phase_end = np.unwrap(np.angle(H_end))
    phase_diff = np.subtract(phase_end, phase_start)
    phase_diff = phase_diff[Q1:Q2]

    p = np.polyfit(x, phase_diff, 1)
    phase_gradient = p[0]
    
    # magnitude
    mag_start = np.abs(H_start)
    mag_end = np.abs(H_end)

    # block arithmetic
    P = N + K
    padded_sequence = pad_so_divisible(received_sequence, P)
    sequence_length = len(padded_sequence)
    num_blocks = int(sequence_length / P)

    demodulated_sequence = []

    for i in range(0, num_blocks):
        lower_index = i * P
        upper_index = lower_index + P

        # estimate interpolation
        H_arr_block = gen_H_estimate(mag_start, mag_end, phase_start, phase_end, i, num_blocks)
        phase_gradient_in_block = phase_gradient * (num_blocks - 2*i) / 2 

        block = padded_sequence[lower_index : upper_index]
        demodulated_block = demodulate_block(block, H_arr_block, N, K, Q1, Q2, phase_gradient_in_block)

        demodulated_sequence = np.concatenate((demodulated_sequence, demodulated_block))

    return demodulated_sequence
