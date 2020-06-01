from src.audio.recording import Recording
from src.file_io.utils import get_data_file_path, get_output_file_path


def num_bit_errors(byte_a, byte_b):
    """Calculate number of bit errors"""
    byte_string_a = format(byte_a, "08b")
    byte_string_b = format(byte_b, "08b")
    
    bit_errors = 0
    for i in range(0, 8):
        if byte_string_a[i] != byte_string_b[i]:
            bit_errors += 1

    return bit_errors


def run():
    """main loop"""
    source_file = input("Source file: ")
    source_file = get_data_file_path(source_file)

    file_obj = open(source_file, mode="rb")
    source_bytes = file_obj.read()
    file_obj.close()

    
    out_file = input("Output file: ")
    out_file = get_output_file_path(out_file)

    file_obj = open(out_file, mode="rb")
    out_bytes = file_obj.read()
    file_obj.close()


    num_bytes = min(len(source_bytes), len(out_bytes))
    
    bit_errors = 0
    
    for i in range(0, num_bytes):
        bit_errors += num_bit_errors(source_bytes[i], out_bytes[i])
            
    bit_error_rate = (bit_errors * 100) / (num_bytes * 8)
    print("Bit error rate: {}%".format(bit_error_rate))


if __name__ == "__main__":
    print("\nTeam Wapiti - Bit Error Rate\n~~~~~~~~~~~~~~~~~~~\n")
    run()
