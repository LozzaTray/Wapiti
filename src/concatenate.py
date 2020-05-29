"""code to generate artificial recording for transmitting known data"""
from src.audio.recording import Recording
from src.file_io.utils import get_recording_file_path


def run():
    """main loop"""
    print("Concatenates wav files A + B")

    file_a = input("File A (.wav): ")
    file_a = get_recording_file_path(file_a + ".wav")
    rec_a = Recording.from_file(file_a)

    file_b = input("File B (.wav): ")
    file_b = get_recording_file_path(file_b + ".wav")
    rec_b = Recording.from_file(file_b)

    rec_a.append_recording(rec_b)

    file_c = input("Save new file under (.wav): ")
    file_c = get_recording_file_path(file_c + ".wav")
    rec_a.save(file_c)

    print("Done")




if __name__ == "__main__":
    print("\nTeam Wapiti - Concatenate\n~~~~~~~~~~~~~~~~~~~\n")
    run()
