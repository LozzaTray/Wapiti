from src.audio.recording import Recording
import matplotlib.pyplot as plt
import numpy as np


def _gen_title_string(recording: Recording, title: str) -> str:
    """generates title string for graph"""
    title = "{} (Rate: {} Hz, {}-channels)".format(title, recording.rate, recording.channels)
    return title


def _gen_time_array(num_samples: int, rate: int):
    """generates time array"""
    time = np.linspace(0, num_samples / rate, num=num_samples)
    return time


def plot_recording(recording: Recording, title="") -> None:
    """displays recording"""
    if isinstance(recording, Recording) == False:
        raise TypeError("Supplied argument is not instance of {}".format(Recording))

    plt.figure()
    plt.title(_gen_title_string(recording, title))
    
    signal = recording.get_frames_as_int16()
    time = _gen_time_array(len(signal), recording.rate)
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
    reference = reference_recording.get_frames_as_int16()

    signal_time = _gen_time_array(len(signal), signal_recording.rate)
    reference_time = _gen_time_array(len(reference), reference_recording.rate)

    correlation = signal_recording.correlate(reference_recording)

    plt.figure()
    plt.subplot(311)
    plt.plot(signal_time, signal)
    plt.subplot(312)
    plt.plot(reference_time, reference)
    plt.subplot(313)
    plt.plot(signal_time, correlation)
    plt.show()
