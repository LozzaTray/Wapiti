"""module for reading and writing wav files"""
import wave
import pyaudio


def read_wav(filename):
    """
    Reads in a wav file
    Accepts:
        filename (string)
        chunk_size (int?)
    Returns:
        data_sequence (?), 
        sample_width (in), 
        num_channels (int), 
        frame_rate (int)
    """

    wf = wave.open(filename, 'rb') #open file for reading
    num_frames = wf.getnframes()
    data_sequence = wf.readframes(num_frames)

    return data_sequence, wf.getsampwidth(), wf.getnchannels(), wf.getframerate()


def write_wav(filename, frames, channels, rate, wav_format):
    """
    Writes out a wav file
    Accepts:
        filename (str)
        frames (b'')
        channels (int)
        rate (num)
        wav_fromat (pyaudio.format)
    """

    #create file from datastream
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(pyaudio.get_sample_size(wav_format))
    wf.setframerate(rate)
    wf.writeframes(frames)
    
    #clean up
    wf.close()