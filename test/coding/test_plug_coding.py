from src.coding.encode import encode_bit_sequence
from src.coding.decode import decode_bit_sequence
import numpy as np


def test_recovery():
    """simple check for the decoder, unlikely to fail"""
    bit_string = b"00011110"
    coded = encode_bit_sequence(bit_string)
    retrieved = decode_bit_sequence(bit_string)
    assert bit_string == retrieved