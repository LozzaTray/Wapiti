from src.coding.encode import encode_bit_string, encode_bits
import pytest
import numpy as np


def test_encode_bits():
    """check each symbol maps as expected"""
    assert encode_bits(format(0, '02b')) == +1+1j
    assert encode_bits(format(1, '02b')) == -1+1j
    assert encode_bits(format(3, '02b')) == -1-1j
    assert encode_bits(format(2, '02b')) == +1-1j
    

def test_encode_bit_string():
    """simple check for the encoder, unlikely to fail"""
    bit_string = '00011110'
    expected = [1+1j, -1+1j, -1-1j, 1-1j]
    response = encode_bit_string(bit_string)
    assert np.allclose(response, expected) == True



def test_encode_bit_string_fails():
    """check error raised"""
    with pytest.raises(ValueError):
        encode_bit_string(format(1, '03b'))

test_encode_bits()
test_encode_bit_string()
test_encode_bit_string_fails()