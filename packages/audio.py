import pyaudio
import wave


def record(length, filename, rate = 44100, size = 1024, channels = 2, FORMAT = pyaudio.paInt16):
    """records audio and saves it to a file.
    Parameters: length (int, seconds), filename (string)"""

    audio = pyaudio.PyAudio()
 
    # start Recording
    stream = audio.open(format=FORMAT, channels=channels, rate=rate, input=True, frames_per_buffer=size)
    print ("recording...")
    frames = []
 
    for i in range(0, int(rate / size * length)):
        data = stream.read(size)
        frames.append(data)
    print ("finished recording")
 
 
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
 
    waveFile = wave.open(filename, 'wb')
    waveFile.setnchannels(channels)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(rate)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()