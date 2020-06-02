from src.file_io.utils import get_output_file_path
from scipy.io import wavfile
import numpy as np


def run():
    """main loop"""    
    out_file = "Group4-C1.bin"
    out_file = get_output_file_path(out_file)

    file_obj = open(out_file, mode="rb")
    out_bytes = file_obj.read()
    file_obj.close()

    data_bit_string = "".join([format(byte, "08b") for byte in out_bytes])

    new_data = []
    for i in range(0, len(data_bit_string), 16):
        new_data.append(data_bit_string[i:i+16])  
    
    int_data = [] 
    for i in new_data:
        int_data.append(int(i,2)-2**15)
    
    filename = get_output_file_path("gr4-decoded.wav")
    wavfile.write(filename, 48000, np.array(int_data, dtype=np.int16))
    print("Done")


if __name__ == "__main__":
    print("\nTeam Wapiti - Group 4 conversion\n~~~~~~~~~~~~~~~~~~~\n")
    run()