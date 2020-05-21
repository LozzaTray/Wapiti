from src.audio.recording import Recording
from src.plotting.utils import gen_time_array
import matplotlib.pyplot as plt
import numpy as np


def gen_title_string(recording: Recording, title: str) -> str:
    """generates title string for graph"""
    title = "{} (Rate: {} Hz, {}-channels)".format(title, recording.rate, recording.channels)
    return title


def plot_recording(recording: Recording, title="") -> None:
    """displays recording"""
    if isinstance(recording, Recording) == False:
        raise TypeError("Supplied argument is not instance of {}".format(Recording))

    plt.figure()
    plt.title(gen_title_string(recording, title))
    
    signal = recording.get_frames_as_int16()
    time = gen_time_array(len(signal), recording.rate)
    plt.plot(time, signal)
    plt.xlabel("Time (s)")
    plt.ylabel("Sample Magnitude")
    plt.grid()

    plt.show()


def plot_correlation(signal_recording: Recording, reference_recording: Recording) -> None:
    """Performs correlation of signal with reference and plots"""
    
    if isinstance(signal_recording, Recording) == False:
        raise TypeError("Signal is not instance of {}".format(Recording))

    if isinstance(reference_recording, Recording) == False:
        raise TypeError("Reference is not instance of {}".format(Recording))
    
    signal = signal_recording.get_frames_as_int16()
    signal_time = gen_time_array(len(signal), signal_recording.rate)

    correlation = signal_recording.correlate(reference_recording)
    correlation_time = gen_time_array(len(correlation), signal_recording.rate)

    fig, (ax1, ax2) = plt.subplots(2, sharex=True)
    fig.suptitle(gen_title_string(signal_recording, "Correlation of signal with reference"))

    ax1.plot(signal_time, signal)
    ax1.set(title="Signal", ylabel="Sample (int16)")

    ax2.plot(correlation_time, correlation)
    ax2.set(title="Correlation", ylabel="Correlation (int64)", xlabel="Time (s)")

    plt.show()
    
    
def plot_schmidl(signal_recording: Recording, N) -> None:
    """Performs correlation of signal with reference and plots"""
    
    if isinstance(signal_recording, Recording) == False:
        raise TypeError("Signal is not instance of {}".format(Recording))
    
    signal = signal_recording.get_frames_as_int16()
    #signal_time = gen_time_array(len(signal), signal_recording.rate)
    
    schmidled = signal_recording.schmidl_correlate(N)
    #schmidled_time = gen_time_array(len(schmidled), signal_recording.rate)
    sig_rate = signal_recording.rate

    fig, (ax1, ax2) = plt.subplots(2, sharex=True)
    fig.suptitle(gen_title_string(signal_recording, "Signal with Schmidl correlation"))

    ax1.plot(signal)
    ax1.set(title="Signal", ylabel="Sample (int16)")
    
    ax2.plot(schmidled)
    ax2.set(title="Schmidl correlation", ylabel="Schmidl correlation (int64)", xlabel="Time (s)")
    
    plt.grid('x', markevery=sig_rate)
    
    plt.show()
    