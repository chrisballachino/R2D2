#!/usr/bin/python

import pyaudio
import wave
import pygame
import time
import sys
import os
import random

def play_noise_old(filename):
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

def play_noise_2(filename):
    print('Should be playing %s'%filename)
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    time.sleep(2)

def play_noise(filename):
    print('Should be playing %s'%filename)
    pygame.mixer.init()
    sounda = pygame.mixer.Sound(filename)
    sounda.play()
    time.sleep(2)    

def random_sound(directory):
    return '%s%s'%(directory,random.choice(os.listdir(directory)))

if __name__=='__main__':
    if(len(sys.argv)==1):
        play_noise_2('/home/pi/r2/sounds/CHORTLE.wav')
    elif(len(sys.argv)==3 and sys.argv[2]=='random'):
        play_noise_2(random_sound(sys.argv[1]))
    else:
        play_noise_2(sys.argv[1])    
