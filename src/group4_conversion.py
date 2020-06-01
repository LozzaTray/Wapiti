from src.file_io.utils import get_output_file_path
from src.audio.recording import Recording
import numpy as np


def run():
    """main loop"""    
    out_file = "Group4-C1.bin"
    out_file = get_output_file_path(out_file)

    file_obj = open(out_file, mode="rb")
    out_bytes = file_obj.read()
    file_obj.close()

    int_array = np.fromstring(out_bytes, np.int16)
    scaled_array = int_array - 2**15

    filename = get_output_file_path("gr4-decoded.bin")
    scaled_array.astype(np.int16).tofile(filename)
    print("Done")


if __name__ == "__main__":
    print("\nTeam Wapiti - Group 4 conversion\n~~~~~~~~~~~~~~~~~~~\n")
    run()