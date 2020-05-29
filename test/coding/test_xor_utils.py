from src.coding.utils import xor
from src.file_io.utils import get_data_file_path

def test_xor():
    binr = open(get_data_file_path("random_bits.txt")).read()[:8]
    test1, N1 = "0000000000000000", 8
    result1 = xor(test1, N1)
    test2, N2 = "000000000000000000", 8
    result2 = xor(test2, N2)
    test3, N3 = "110011001100110000", 8
    result3 = xor(test3, N3)
    actual_result3 = "0010111000101110" + binr

    assert(result1 == binr*2)
    assert(result2 == binr*3)
    assert(result3 == actual_result3)