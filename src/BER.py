from src.audio.recording import Recording
from src.file_io.utils import get_recording_file_path


def run():
    """main loop"""
    file1_short = input("File name to open (.wav): ")
    file1_full = get_recording_file_path(file1_short + ".wav")

    seq1 = Recording.from_file(file1_full).get_frames_as_int16()
    
    file2_short = input("File name to open (.wav): ")
    file2_full = get_recording_file_path(file2_short + ".wav")

    seq2 = Recording.from_file(file2_full).get_frames_as_int16()

    assert(len(seq2)==len(seq1)), "Bit sequences are not of the same length"
    
    errors = 0
    bits = 0
    
    for i in range(len(seq1)):
        for j in range(16):
            if str(bin(seq1[i]))[2:].zfill(16)[j] != str(bin(seq2[i]))[2:].zfill(16)[j]:
                errors += 1
            bits += 1
            
    print("bit error rate: {}%".format(errors*100/bits))


if __name__ == "__main__":
    print("\nTeam Wapiti - Bit Error Rate\n~~~~~~~~~~~~~~~~~~~\n")
    run()
