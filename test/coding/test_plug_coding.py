from src.coding.encode import encode_bit_string
from src.coding.decode import decode_symbol_sequence
import numpy as np


def test_recovery():
    """simple check for the encoder -> decoder compatibility, unlikely to fail"""
    bit_string = b"00011110"
    coded = encode_bit_string(bit_string)
    retrieved = decode_symbol_sequence(coded)
    assert bit_string == retrieved