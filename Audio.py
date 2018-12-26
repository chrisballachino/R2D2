#!/usr/bin/python

import pyaudio
import wave

def play_noise(filename):
    #define stream chunk
    chunk = 1024

    f = wave.open(filename,"rb")

    #instantiate pyaudio
    p = pyaudio.PyAudio()

    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                    channels = f.getnchannels(),
                    rate = f.getframerate(),
                    output = True)

    #read data
    data = f.readframes(chunk)

    #play stream
    while(data):
        stream.write(data)
        data = f.readframes(chunk)

    #stop stream
    stream.stop_stream()
    stream.close()

    #close pyaudio
    p.terminate()

if __name__=='__main__':
    play_noise('./sounds/WHIST2.wav')    
