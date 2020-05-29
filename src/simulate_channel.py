"""Code for simulating a virtual channel"""
from src.audio.recording import Recording
from src.file_io.utils import get_output_file_path, get_data_file_path
from src.plotting.plot_recording import plot_recording


def run():
    """main loop"""
    signal_file = input("Signal to load (.wav): ")
    signal_file = get_data_file_path(signal_file + ".wav")
    signal = Recording.from_file(signal_file)

    channel = [0.5 , 0.2 , 0, 0.1, 0.04, 0]

    print("Passing through channel...")
    received_signal = signal.pass_through_channel(channel)
    print("Done")

    out_file = input("File name to save (.wav): ")
    out_file = get_output_file_path(out_file + ".wav")
    received_signal.save(out_file)

    plot_recording(signal, "Original Signal")
    plot_recording(received_signal, "Signal after passing through simulated channel")

if __name__ == "__main__":
    print("\nTeam Wapiti - Simulate\n~~~~~~~~~~~~~~~~~~~\n")
    run()
