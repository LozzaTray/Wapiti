from src.coding.encode import encode_bit_sequence


def test_encode_bit_sequence():
    """simple check for the decoder, unlikely to fail"""
    sym1 = complex(1, 1)
    sym2 = complex(-1, 1)
    sym3 = complex(-1, -1)
    sym4 = complex(1, -1)
    response = [decode_symbol(sym1), decode_symbol(sym2), decode_symbol(sym3), decode_symbol(sym4)]
    assert response == [[0, 0], [0, 1], [1, 1], [1, 0]]
    print("Pass")


def test_bit_array_to_byte():
    bit_array1 = [0, 0, 0, 0, 0, 0, 0, 0]
    bit_array2 = [1, 0, 1, 0, 1, 0, 1, 0]
    bit_array3 = [0, 1, 0, 1, 0, 1, 0, 1]
    bit_array4 = [1, 1, 1, 0, 0, 0, 0]
    response = [bit_array_to_byte(bit_array1), bit_array_to_byte(bit_array2), bit_array_to_byte(bit_array3)]
    assert response == [0b00000000, 0b10101010, 0b01010101]
    try:
        bit_array_to_byte(bit_array4)
    except ValueError:
        pass
    print("Pass")


def test_parse_byte_sequence():
    sequence = [78, 105, 99, 101, 0, 51, 0, 33, "Number", 0b00110101]
    title,length,file = parse_byte_sequence(sequence)
    assert title == 'Nice'
    assert length == 3
    assert file == sequence[7:10]
    print("Pass")
