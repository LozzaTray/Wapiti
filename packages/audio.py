import pyaudio
import wave

def record(length, filename, rate = 44100, chunk = 1024, channels = 2, FORMAT = pyaudio.paInt16):
    """records audio and saves it to a file.
    Parameters: length (int, seconds), filename (string)"""

    audio = pyaudio.PyAudio() #create pyaudio object

    #start recording
    stream = audio.open(format=FORMAT, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    print ("Recording...")
    frames = []
 
    #write audio data to a stream
    for i in range(0, int(rate / chunk * length)):
        data = stream.read(chunk)
        frames.append(data)
    print ("Finished recording")
 
    #stop recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
 
    #create file from datastream
    waveFile = wave.open(filename, 'wb')
    waveFile.setnchannels(channels)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(rate)
    waveFile.writeframes(b''.join(frames))
    
    #clean up
    waveFile.close()
    
    return frames
    
def playback(filename, chunk=1024):
    """play audio from wav file given filename (string)"""
    
    wf = wave.open(filename, 'rb') #open file for reading
    p = pyaudio.PyAudio() #create pyaudio object
    
    #open stream based on the input wave object
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)

    data = wf.readframes(chunk) #read data
    
    #play audio
    while data != b'':
        stream.write(data) #writing to the stream is what actually plays the sound
        data = wf.readframes(chunk)
        
    print("EHWER")
    
    #cleanup
    stream.close()    
    p.terminate()
    
    print("dsfsdsdfsdf")
