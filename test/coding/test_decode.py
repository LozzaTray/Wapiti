from src.coding.decode import decode_symbol_sequence


def test_decode_symbol_sequence():
    """simple check for the decoder, unlikely to fail"""
    symbol_arr = [1+1j, -1+1j, -1-1j, 1-1j]
    response_bit_string = decode_symbol_sequence(symbol_arr)
    expected_bit_string = "00011110"
    assert response_bit_string == expected_bit_string