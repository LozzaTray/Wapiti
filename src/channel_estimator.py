"""code to generate artificial recording for transmitting known data"""
from src.audio.recording import Recording
from src.plotting.plot_recording import plot_recording
from src.file_io.utils import get_output_file_path
from src.ofdm.estimate_channel import estimate_channel
from src.plotting.impulse_response import plot_h_in_time, plot_h_freq_domain


def run():
    """main loop"""
    #constants
    N = 1024
    K = 1000

    # get data pre-transmission
    sent_file = input("Data that was sent (.wav): ")
    sent_file = get_output_file_path(sent_file + ".wav")
    data_rec = Recording.from_file(sent_file)
    #sampling_freq = data_rec.rate
    
    data_seq = data_rec.get_frames_as_int16()
    D = len(data_seq)
    

    received_file = input("Recorded transmission (.wav): ")
    received_file = get_output_file_path(received_file + ".wav")
    received_rec = Recording.from_file(received_file)


    reference_file = input("Reference signal (.wav): ")
    reference_file = get_output_file_path(reference_file + ".wav")
    reference_rec = Recording.from_file(reference_file)

    received_data = received_rec.extract_data_sequence(reference_rec, D)

    h = estimate_channel(received_data, data_seq, N=1024, K=1000)

    plot_h_in_time(h)
    plot_h_freq_domain(h, N=N)



if __name__ == "__main__":
    print("\nTeam Wapiti - Creating Data\n~~~~~~~~~~~~~~~~~~~\n")
    run()
