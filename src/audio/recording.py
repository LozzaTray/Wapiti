"""module for recording and playing wav objects"""
import pyaudio
from src.file_io.wav import read_wav, write_wav
from scipy.signal import correlate as scipy_correlate
import matplotlib.pyplot as plt
import numpy as np


class Recording:

    # Default props
    DEFAULT_RATE = 48000
    DEFAULT_CHUNK = 1024
    DEFAULT_NUM_CHANNELS = 1
    DEFAULT_FORMAT = pyaudio.paInt16


    def __init__(self, frames, rate, num_channels, audio_format):
        self.frames = frames
        self.rate = rate
        self.channels = num_channels
        self.audio_format = audio_format


    @classmethod
    def from_mic(cls, duration, num_channels=DEFAULT_NUM_CHANNELS, rate=DEFAULT_RATE, chunk=DEFAULT_CHUNK, audio_format=DEFAULT_FORMAT):
        """Initialise recording from mic"""

        p = pyaudio.PyAudio() #create pyaudio object

        #start recording
        stream = p.open(
            format=audio_format, 
            channels=num_channels,
            rate=rate,
            frames_per_buffer=chunk,
            input=True
        )

        frames = []
        print ("Recording...")

        #read audio data from stream
        for i in range(0, int(rate / chunk * duration)):
            data = stream.read(chunk)
            frames.append(data)
        
        print ("Finished recording")
        frames = b"".join(frames)
    
        #stop recording
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
        data_sequence, sample_width, num_channels, frame_rate = read_wav(original_file)

        return cls(
            frames=data_sequence,
            rate=frame_rate,
            num_channels=num_channels,
            audio_format=pyaudio.get_format_from_width(sample_width)
        )
       
        
    @classmethod
    def from_list(cls, data_sequence, frame_rate):
        """Initialise audio from list"""
        bit_string = b"".join(data_sequence.astype(np.int16))
        return cls(
            frames = bit_string, 
            rate = frame_rate,
            num_channels=1,
            audio_format=pyaudio.paInt16
        )


    def play(self):
        """Plays the specified recording"""
        #create pyaudio object
        p = pyaudio.PyAudio() 
        
        #open audio stream
        stream = p.open(
            format = self.audio_format,
            channels = self.channels,
            rate = self.rate,
            output = True
        )

        stream.write(self.frames)
        
        #cleanup
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


    def display(self, title=""):
        """Displays recording"""
        plt.figure()
        
        plt.title("{} (Rate: {} Hz, {}-channels, 16-bit signed int)".format(title, self.rate, self.channels))
        
        signal = self.get_frames_as_int16()
        time = np.linspace(0, len(signal) / self.rate, num=len(signal))
        plt.plot(time, signal)
        plt.xlabel("Time (s)")
        plt.ylabel("Sample Magnitude")
        plt.grid()

        plt.show()


    def correlate(self, reference_recording):
        signal = self.get_frames_as_int16()
        reference = reference_recording.get_frames_as_int16()
        correlation = scipy_correlate(signal, reference, mode="valid")

        self.display("Real signal")
        self.display("Reference signal")

        plt.figure()
        plt.plot(correlation)
        plt.show()


    def get_frames_as_int16(self):
        return np.fromstring(self.frames, np.int16)
