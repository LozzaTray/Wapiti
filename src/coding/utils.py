from src.file_io.utils import get_data_file_path


def text_to_bin(text):
    binary = format(int.from_bytes(text[0].encode(), "big"), '08b')
    for i in range(len(text) - 1):
        binary += format(int.from_bytes(text[i + 1].encode(), "big"), '08b')

    return binary


def xor(bin_data, N):
    binr = open(get_data_file_path("random_bits.txt")).read()[:N]
    if len(bin_data)%N != 0:
        bin_data = bin_data + ("0" * (N - (len(bin_data) % N)))

    i = 0
    all_xored = ""
    while i < len(bin_data):
        xored_data = format(int(bin_data[i:i + N], 2) ^ int(binr, 2), '0' + str(N) + 'b')
        all_xored += xored_data
        i += N
    return all_xored
