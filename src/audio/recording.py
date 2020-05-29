"""module for recording and playing wav objects"""
from config import F, N, K, C, D, W, F0, F1
from src.file_io.wav import read_wav, write_wav
from src.ofdm.estimate_channel import estimate_channel, calc_abs_angle_error
from src.file_io.utils import get_output_file_path
from src.plotting.impulse_response import plot_h_freq_domain, plot_h_in_time
import pyaudio
import scipy.signal as scipy_signal
import numpy as np
import math
import matplotlib.pyplot as plt


class Recording:
    # Default props
    DEFAULT_RATE = F
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

    @classmethod
    def empty(cls, frame_rate):
        return cls(
            frames=b"",
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

    def extract_packets(self, delimiter_rec):
        """
        Extract data packets as an array of sequences each of length (D+W+D)*P
        returns:
            packet_arr: [ int16[] ] - array of packet data sequences
            dither_arr: [ int ] - array of dithers for each packet
        """
        #constant declaration
        P = N + K
        DATA_WIDTH = (D + W + D) * P
        PEAK_SEPARATION = DATA_WIDTH + C * P

        # termination constants
        MAX_PEAK_DELAY = 50
        MAGNITUDE_THRESHOLD = 0.5

        correlation_arr = np.abs(self.correlate(delimiter_rec))
        
        signal_arr = self.get_frames_as_int16()
        data_length = len(signal_arr)

        packet_arr = []
        dither_arr = []

        current_peak_index = np.argmax(correlation_arr[0 : W * P])
        current_peak_value = correlation_arr[current_peak_index]

        while (True):
            next_peak_lower_bound = current_peak_index + PEAK_SEPARATION - MAX_PEAK_DELAY
            next_peak_upper_bound = next_peak_lower_bound + 2 * MAX_PEAK_DELAY

            if(next_peak_lower_bound >= data_length):
                print("Reached end of recording")
                break

            correlation_arr_about_next_peak = correlation_arr[ next_peak_lower_bound : next_peak_upper_bound]
            relative_index = np.argmax(correlation_arr_about_next_peak)
            next_peak_value = correlation_arr_about_next_peak[relative_index]

            if(next_peak_value <= MAGNITUDE_THRESHOLD * current_peak_value):
                print("No peaks of sufficient magnitude found, end of data declared")
                break

            # Dither
            dither = relative_index - MAX_PEAK_DELAY
            dither_arr.append(dither)

            # Packet
            data_start_index = current_peak_index + 1
            packet_data = signal_arr[data_start_index : data_start_index + DATA_WIDTH]
            packet_arr.append(packet_data)

            # update vars
            current_peak_index = next_peak_lower_bound + relative_index
            current_peak_value = next_peak_value

        return packet_arr, dither_arr
    
    def sync_chirp(self, signal_file):
        """Find data sequences based on matched filter convolution with a chirp
        signal_file - path/name.wav"""
        
        #constants
        P = N + K
        WP = W * P
        
        #parameters
        samples_threshold = 0.05 #tolerance in position of peaks
        magnitude_threshold = 0.8 #tolerance in size of magnitude of convolution peak compared with previous
        
        reference__chirp_file = 'c' #input("Reference signal (.wav): ")
        reference__chirp_file = get_output_file_path(reference__chirp_file + ".wav")
        reference__chirp = Recording.from_file(reference__chirp_file)
        
        signal = Recording.from_file(signal_file)
    
        c = signal.correlate(reference_chirp)
        plt.plot(c)
        
        signalList = signal.get_frames_as_int16() 
    
        i = 0
        data = []
    
        while True:
            c_trunc = c[i:i+WP] #obtain a truncated peak
            print(i, i+WP)
             
            #find index and value of maximum value of correlation output
            peak_index_t = np.argmax(c_trunc)
            peak_value = c_trunc[peak_index_t]
            peak_index = i + peak_index_t
            
            print("PEAK:", peak_index)
            
            #if there are not enough samples for another transmission, end the process
            if len(c) < int(peak_index+225*P*(1-samples_threshold)):
                print("not enough samples remaining for another signal")
                break
            
            #if there is not another peak of similar magnitude after 220P±1% samples, end the process
            next_peak_range = c[int(peak_index+220*P*(1-samples_threshold)):int(peak_index+220*P*(1+samples_threshold))]
            print("search range:", int(peak_index+220*P*(1-samples_threshold)), int(peak_index+220*P*(1+samples_threshold)))
            if np.max(c[peak_index:peak_index+len(next_peak_range)]) < peak_value*magnitude_threshold:
                print("no chirp detected")
                break
            
            data.append(signalList[peak_index:peak_index+220*P]) #append list of data values between chirp
            i+=int(220*P*(1-samples_threshold)) #increase index by 220P-1% samples from previous peak
            
        print("DATA SEQUENCES FOUND:", len(data))
        