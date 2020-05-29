from config import OUTPUT_DIR, DATA_DIR
import os


def get_output_file_path(file_name_short):
    return os.path.join(OUTPUT_DIR, file_name_short)


def get_data_file_path(file_name_short):
    return os.path.join(DATA_DIR, file_name_short)


def progress_bar(current, total,  barLength = 20):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))

    print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')