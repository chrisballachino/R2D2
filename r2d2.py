#!/usr/bin/python

import os,sys
import RPi.GPIO as GPIO
import faulthandler
import socket
import struct

from Controller import *
from Motor import *
from Audio import *

########## Set up everything ##############
def setup_raspberry_pi():
    GPIO.setmode(GPIO.BCM)

#Note: not necessary anymore, using UDP
def setup_motors():
    left_wheel = Motor(0)
    right_wheel = None#Motor(1)
    dome = None#Motor(2)

    left_wheel.init()
    
    return (left_wheel,right_wheel,dome)

def setup_controller():
    controller = ps4_controller()
    return controller

def setup_leds():
    pass #TODO

def setup_audio():
    pass #shouldn't have to do anything

def setup_udp():
    return socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

###########################################

if __name__=='__main__':
    UDP_IP = '127.0.0.1'
    UDP_PORT_LEFT = 7777
    UDP_PORT_RIGHT = 7778
    UDP_PORT_DOME = 7779

    faulthandler.enable()
    setup_raspberry_pi()
    #(left_wheel,right_wheel,dome) = setup_motors()
    controller = setup_controller()
    setup_leds()
    setup_audio()
    sock = setup_udp()
    firstTime = True

    counter = 0    
    
    while(True):
        output = controller.read()

        #TODO this could be much cleaner as a loop, clean up if there's time and will
	#joystick outputs a tuple of tuples
	if(output != None and len(output)==2 and type(output[0])==tuple):
            (keyTypeY,keyValY) = output[0]
            (keyTypeX,keyValX) = output[1]

            #if this is a joystick, read the 'y' component
            if(keyTypeY == 'ly' or keyTypeY == 'ry'):
                #print('%s: %.3f'%(keyTypeY,keyValY))
                #if it's 0, stop moving
                if(keyValY == 0.0):
                    data = (0,1)
                    packed_data = bytes()
                    packed_data = packed_data.join((struct.pack('B',val) for val in data))
                    if(keyTypeY == 'ly'):
                        sock.sendto(packed_data,(UDP_IP,UDP_PORT_LEFT))
                    else:
                        sock.sendto(packed_data,(UDP_IP,UDP_PORT_RIGHT))
                #we want to move
                else:
                    #direction (negative is forward)
                    if(keyTypeY == 'ly'):
                        if(keyValY < 0.0):
                            direction = 1
                        else:
                            direction = 0
                    #for some reason the two motors are backwards
                    else:
                        if(keyValY < 0.0):
                            direction = 0
                        else:
                            direction = 1

                    #joystick returns -1.0 to 1, so multiply to get 0 to 100
                    speed = int(abs(keyValY)*100)
                    print('Y Speed = %i, direction = %i'%(speed,direction))

                    data = (speed,direction)                
                    packed_data = bytes()
                    packed_data = packed_data.join((struct.pack('B',val) for val in data))

                    if(keyTypeY == 'ly'):
                        sock.sendto(packed_data,(UDP_IP,UDP_PORT_LEFT))                
                    else:
                        sock.sendto(packed_data,(UDP_IP,UDP_PORT_RIGHT))
            if(keyTypeX == 'lx'): #Only use one joystick to avoid sending two directions back-to-back # or keyTypeX == 'rx'):
                #print('%s %.3f'%(keyTypeX,keyValX))
                if(abs(keyValX) < 5.0):
                    data = (0,1)
                    packed_data = bytes()
                    packed_data = packed_data.join((struct.pack('B',val) for val in data))
                    sock.sendto(packed_data,(UDP_IP,UDP_PORT_DOME))
                else:
                    #direction (negative is left)
                    if(keyValX < 0.0):
                        direction = 1
                    else:
                        direction = 0
             
                    speed = int(abs(keyValX)*100)
                    print('X Speed = %i, direction = %i'%(speed,direction))

                    data = (speed,direction)
                    packed_data = bytes()
                    packed_data = packed_data.join((struct.pack('B',val) for val in data))
                    sock.sendto(packed_data,(UDP_IP,UDP_PORT_DOME))
            
        else:
            try:
                (keyType,keyVal) = output
                print('%s: %i'%(keyType,keyVal))
                if(keyType == 'x' and keyVal == 1):
                    play_noise('./sounds/RAZZ10.wav')
                elif(keyType == 'square' and keyVal == 1):
                    play_noise('./sounds/CHORTLE.wav')
                elif(keyType == 'triangle' and keyVal == 1):
                    play_noise('./sounds/GROAN.wav')
                elif(keyType == 'circle' and keyVal == 1):
                    play_noise('./sounds/WOWIE.wav')
            except:
                print('Key not valid:')
                print(output)
