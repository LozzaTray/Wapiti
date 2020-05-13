from src.ofdm.utils import dft, idft, insert_cyclic_prefix, pad_so_divisible


def test_dft():
    N = 3
    x = [0, 0, 1]
    y = dft(x, N)
    assert len(y) == N

    N = 2
    y = dft(x, N)
    assert len(y) == N
    assert list(y) == list([0, 0])


def test_idft():
    N = 3
    x = [0, 0, 1]
    y = idft(x, N)
    assert len(x) == N

    N = 2
    y = idft(x, N)
    assert len(y) == N
    assert list(y) == list([0, 0])


def test_insert_cyclic_prefix():
    K = 2
    x = [1, 2, 3]
    y = insert_cyclic_prefix(x, K)
    assert list(y) == list([2, 3, 1, 2, 3])


def test_pad_so_divisible():
    M = 6
    x = [1, 2, 3, 4]
    y = pad_so_divisible(x, M)
    assert list(y) == list([1, 2, 3, 4, 0, 0])
