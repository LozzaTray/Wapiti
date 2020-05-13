"""module for recording and playing wav objects"""
import pyaudio
from src.file_io.wav import read_wav, write_wav
import matplotlib.pyplot as plt
import numpy


class Recording:

    # Default props
    DEFAULT_RATE = 48000
    DEFAULT_CHUNK = 1024
    DEFAULT_CHANNELS = 2
    DEFAULT_FORMAT = pyaudio.paInt16


    def __init__(self, frames, rate, channels, audio_format):
        self.frames = frames
        self.rate = rate
        self.channels = channels
        self.audio_format = audio_format


    @classmethod
    def from_mic(cls, duration, channels=DEFAULT_CHANNELS, rate=DEFAULT_RATE, chunk=DEFAULT_CHUNK, audio_format=DEFAULT_FORMAT):
        """Initialise recording from mic"""

        p = pyaudio.PyAudio() #create pyaudio object

        #start recording
        stream = p.open(
            format=audio_format, 
            channels=channels,
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
            channels=channels,
            audio_format=audio_format
        )


    @classmethod
    def from_file(cls, original_file):
        """Initialise recording from file"""
        data_sequence, sample_width, num_channels, frame_rate = read_wav(original_file)

        return cls(
            frames=data_sequence,
            rate=frame_rate,
            channels=num_channels,
            audio_format=pyaudio.get_format_from_width(sample_width)
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


    def display(self):
        """Displays recording"""
        signal = numpy.fromstring(self.frames, numpy.int16)
        plt.figure(1)
        plt.plot(signal)
        plt.show()
