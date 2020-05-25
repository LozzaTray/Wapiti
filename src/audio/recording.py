"""module for recording and playing wav objects"""
import pyaudio
from src.file_io.wav import read_wav, write_wav
from src.ofdm.estimate_channel import estimate_channel, calc_abs_angle_error
import scipy.signal as scipy_signal
import numpy as np
from config import SAMPLING_FREQ
from src.plotting.impulse_response import plot_h_freq_domain, plot_h_in_time


class Recording:
    # Default props
    DEFAULT_RATE = SAMPLING_FREQ
    DEFAULT_CHUNK = 1024
    DEFAULT_NUM_CHANNELS = 1
    DEFAULT_FORMAT = pyaudio.paInt16

    def __init__(self, frames, rate, num_channels, audio_format):
        self.frames = frames
        self.rate = rate
        self.channels = num_channels
        self.audio_format = audio_format

    @classmethod
    def from_mic(cls, duration, num_channels=DEFAULT_NUM_CHANNELS, rate=DEFAULT_RATE, chunk=DEFAULT_CHUNK,
                 audio_format=DEFAULT_FORMAT):
        """Initialise recording from mic"""

        p = pyaudio.PyAudio()  # create pyaudio object

        # start recording
        stream = p.open(
            format=audio_format,
            channels=num_channels,
            rate=rate,
            frames_per_buffer=chunk,
            input=True
        )

        frames = []
        print("Recording...")

        # read audio data from stream
        for i in range(0, int(rate / chunk * duration)):
            data = stream.read(chunk)
            frames.append(data)

        print("Finished recording")
        frames = b"".join(frames)

        # stop recording
        stream.stop_stream()
        stream.close()
        p.terminate()

        return cls(
            frames=frames,
            rate=rate,
            num_channels=num_channels,
            audio_format=audio_format
        )

    @classmethod
    def from_file(cls, original_file):
        """Initialise recording from file"""
        data_sequence, sample_width, num_channels, frame_rate = read_wav(
            original_file)

        return cls(
            frames=data_sequence,
            rate=frame_rate,
            num_channels=num_channels,
            audio_format=pyaudio.get_format_from_width(sample_width)
        )

    @classmethod
    def from_list(cls, data_sequence, frame_rate):
        """Initialise audio from list"""
        data_sequence = np.array(data_sequence)
        bit_string = b"".join(data_sequence.astype(np.int16))
        return cls(
            frames=bit_string,
            rate=frame_rate,
            num_channels=1,
            audio_format=pyaudio.paInt16
        )

    def play(self):
        """Plays the specified recording"""
        # create pyaudio object
        p = pyaudio.PyAudio()

        # open audio stream
        stream = p.open(
            format=self.audio_format,
            channels=self.channels,
            rate=self.rate,
            output=True
        )

        stream.write(self.frames)

        # cleanup
        stream.close()
        p.terminate()

    def save(self, filename):
        """Saves current recording at the specified file"""
        write_wav(
            filename=filename,
            frames=self.frames,
            channels=self.channels,
            rate=self.rate,
            wav_format=self.audio_format
        )

    def correlate(self, reference_recording):
        """Performs correlation of self with reference_recording"""
        signal = self.get_frames_as_int16()
        reference = reference_recording.get_frames_as_int16()
        # astype(int64) needed to prevent overflow
        correlation = scipy_signal.correlate(signal.astype(np.int64), reference, mode="full")
        return correlation

    def schmidl_correlate(self, N):
        """Performs correlation of self using Schmidl and Cox"""
        signal = self.get_frames_as_int16()
        corr_arr = [0] * self.rate * 3
        #computing corr_arr[0]
        total = 0
        for i in range(N//2 -1):
            total += np.int64(signal[i]) * signal[i+N//2]
        corr_arr[0] = total
        #now compute the rest!
        for i in range(self.rate * 3 -1):
            total -= np.int64(signal[i]) * signal[i+N//2]
            total += np.int64(signal[i+N//2]) * signal[i + N]
            corr_arr[i+1] = total

        return corr_arr

    def extract_data_sequence(self, reference_recording, D, offset=0):
        """
        extracts the data_sequence
        reference_recording - Recording against which to correlate
        D - length of data block following first chirp
        offset - manual offset to start of data sequence
        """
        correlation_arr = self.correlate(reference_recording)
        length = len(correlation_arr)

        # TODO Less hacky
        first_half = np.abs(correlation_arr[0 : length // 2])
        index_of_max = np.argmax(first_half)
        data_arr = self.get_frames_as_int16()

        data_start = index_of_max + 1 + offset
        data_end = data_start + D

        return data_arr[data_start : data_end]

    def extract_data_sequence_schmidl(self, N, K, D, known_block, width = 5):
        """
        extracts the data_sequence from Schmidl and Cox synchronised data
        N - Fourier block size
        K - Cyclic prefix length
        D - length of data block following Schmidl and Cox 'block'
        """
        correlation_arr = self.schmidl_correlate(N)
        index_of_max = np.argmax(np.abs(correlation_arr))
        data_arr = self.get_frames_as_int16()

        for i in range( - width, width + 1):
            lower_index = index_of_max + i - K
            upper_index = lower_index + N + K

            schmidl_block = data_arr[lower_index : upper_index]
            h_estimate = estimate_channel(schmidl_block, known_block, N=N, K=K)

            mse = calc_abs_angle_error(h_estimate, N=N)
            print("offset: {}, mse: {}".format(i, mse))
            #plot_h_freq_domain(h_estimate, N=N)


        data_start = index_of_max + N - 1# can give own shift
        data_end = data_start + D

        return data_arr[data_start : data_end]

    def pass_through_channel(self, channel_impulse_response):
        """simulates passing through a virtual channel and returns a new recording"""
        signal = self.get_frames_as_int16()
        convolved_signal = scipy_signal.convolve(signal, channel_impulse_response)
        return Recording.from_list(convolved_signal, self.rate)

    def get_frames_as_int16(self):
        return np.fromstring(self.frames, np.int16)

    def append_recording(self, rec2):
        """Append two 'Recording' instances together"""

        assert (self.channels == rec2.channels), "Number of channels does not match ({} and {})".format(self.channels,
                                                                                                        rec2.channels)
        assert (self.rate == rec2.rate), "Rates do not match ({} and {})".format(self.rate, rec2.rate)
        assert (self.audio_format == rec2.audio_format), "Audio formats do not match ({} and {})".format(
            self.audio_format, rec2.audio_format)

        self.frames += rec2.frames
