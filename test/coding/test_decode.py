from src.coding.decode import decode_symbol


def test_decode_symbol():
    """simple check for the decoder, unlikely to fail"""
    sym1 = complex(1, 1)
    sym2 = complex(-1, 1)
    sym3 = complex(-1, -1)
    sym4 = complex(1, -1)
    response = [decode_symbol(sym1), decode_symbol(sym2), decode_symbol(sym3), decode_symbol(sym4)]
    assert response == [[0, 0], [0, 1], [1, 1], [1, 0]]