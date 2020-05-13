"""module for reading and writing wav files"""
import wave

def read_wav(filename):
    """reads in a wav file"""
    file = wave.open(filename, mode='rb')
    frames = file.readframes(file.getnframes())
    file_params = file.getparams() #number of channels, sample width (in bytes), framerate, number of frames, compression type, compression name
    return frames, file_params[0:4]


def write_wav(filename):
    """writes out a wav file"""
    raise NotImplementedError
