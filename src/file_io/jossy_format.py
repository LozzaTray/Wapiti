from src.decode_csv import decode_symbol_sequence_jossy_format
from src.ofdm.demodulate import demodulate_sequence
from src.file_io.utils import get_output_file_path


def perform_jossy(data_sequence, impulse_response, N, K):
    """Decodes a data array according to Jossy format"""
    print("Demodulating OFDM...")
    symbol_sequence = demodulate_sequence(data_sequence, impulse_response, N=N, K=K)

    print("Decoding QPSK...")
    title, file_length, file_bytes = decode_symbol_sequence_jossy_format(symbol_sequence)

    print("Successfully decoded: " + title + " (" + str(file_length) + " bytes)")
    
    print("Saving file...")
    output_file = get_output_file_path(title)
    file_bytes.tofile(output_file)