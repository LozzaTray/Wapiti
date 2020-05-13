"""module for reading and writing wav files"""
import wave
import pyaudio


def read_wav_full(filename):
    """reads in a wav file"""
    file = wave.open(filename, mode='rb')
    frames = file.readframes(file.getnframes())
    file_params = file.getparams() #number of channels, sample width (in bytes), framerate, number of frames, compression type, compression name
    return frames, file_params


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
    
    p = pyaudio.PyAudio()
    num_frames = wf.getnframes()
    data_sequence = wf.readframes(num_frames)
    p.terminate()

    return data_sequence, wf.getsampwidth(), wf.getnchannels(), wf.getframerate()


def write_wav(filename, frames, channels, rate, wav_format):
    """writes out a wav file"""
    #create file from datastream
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(pyaudio.get_sample_size(wav_format))
    wf.setframerate(rate)
    wf.writeframes(frames)
    
    #clean up
    wf.close()