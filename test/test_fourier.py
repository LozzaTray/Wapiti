from src.modulation.fourier import dft, idft


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
