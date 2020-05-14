from src.coding.encode import encode_bit_sequence, encode_bits
import pytest
import numpy as np


def test_encode_bits():
    """check each symbol maps as expected"""
    assert encode_bits(b"00") == +1+1j
    assert encode_bits(b"01") == -1+1j
    assert encode_bits(b"11") == -1-1j
    assert encode_bits(b"10") == +1-1j


def test_encode_bits_():
    """check error raised"""
    with pytest.raises(ValueError):
        encode_bits(b"001")
    

def test_encode_bit_sequence():
    """simple check for the decoder, unlikely to fail"""
    bit_string = b"00011110"
    expected = [1+1j, -1+1j, -1-1j, 1-1j]
    response = encode_bit_sequence(bit_string)
    assert np.allclose(response, expected) == True