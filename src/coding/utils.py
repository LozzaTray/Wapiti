

def text_to_bin(text):
    binary = format(int.from_bytes(text[0].encode(), "big"), '08b')
    for i in range(len(text)-1):
        binary += format(int.from_bytes(text[i+1].encode(), "big"), '08b')

    return binary
