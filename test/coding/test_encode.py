from src.coding.encode import encode_bit_string, encode_bits
import pytest
import numpy as np


def test_encode_bits():
    """check each symbol maps as expected"""
    assert encode_bits(b"00") == +1+1j
    assert encode_bits(b"01") == -1+1j
    assert encode_bits(b"11") == -1-1j
    assert encode_bits(b"10") == +1-1j
    

def test_encode_bit_string():
    """simple check for the encoder, unlikely to fail"""
    bit_string = b"00011110"
    expected = [1+1j, -1+1j, -1-1j, 1-1j]
    response = encode_bit_string(bit_string)
    assert np.allclose(response, expected) == True



def test_encode_bit_string_fails():
    """check error raised"""
    with pytest.raises(ValueError):
        encode_bit_string(b"001")