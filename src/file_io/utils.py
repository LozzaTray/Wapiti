from config import OUTPUT_DIR, DATA_DIR
import os


def get_output_file_path(file_name_short):
    return os.path.join(OUTPUT_DIR, file_name_short)


def get_data_file_path(file_name_short):
    return os.path.join(DATA_DIR, file_name_short)