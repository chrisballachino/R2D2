#!/usr/bin/python

import os,sys
import RPi.GPIO as GPIO
import faulthandler

from Controller import *
from Motor import *
from Audio import *

########## Set up everything ##############
def setup_raspberry_pi():
    GPIO.setmode(GPIO.BCM)

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
    pass #TODO

###########################################

if __name__=='__main__':
    faulthandler.enable()
    setup_raspberry_pi()
    (left_wheel,right_wheel,dome) = setup_motors()
    controller = setup_controller()
    setup_leds()
    setup_audio()

    counter = 0    
    
    while(True):
        (keyType,keyVal) = controller.read()

        #if this is a joystick, read the 'y' component
        if(keyType == 'ly' or keyType == 'ry'):
            counter += 1
            if(counter == 100):
                counter = 0
            else:
                continue
            print('%s: %.3f'%(keyType,keyVal))
            #if it's 0, stop moving
            if(keyVal == 0.0):
                left_wheel.engage_motor(True)
                left_wheel.engage_motor(False)
            #we want to move
            else:
                #direction (negative is forward)
                if(keyVal < 0.0):
                    direction = 1
                else:
                    direction = 0

                #joystick returns -1.0 to 1, so multiply to get 0 to 100
                speed = int(abs(keyVal)*100)
                print('Speed = %i, direction = %i'%(speed,direction))

                #set speed
                left_wheel.set_speed(speed,direction)
        else:
            print('%s: %i'%(keyType,keyVal))
            if(keyType == 'x' and keyVal == 1):
                play_noise('./sounds/RAZZ10.wav')
            elif(keyType == 'square' and keyVal == 1):
                play_noise('./sounds/CHORTLE.wav')
            elif(keyType == 'triangle' and keyVal == 1):
                play_noise('./sounds/GROAN.wav')
            elif(keyType == 'circle' and keyVal == 1):
                play_noise('./sounds/WOWIE.wav')
            elif(keyType == 'l1' and keyVal == 1):
                left_wheel.set_speed(25,1)
            elif(keyType == 'r1' and keyVal == 1):
                left_wheel.set_speed(95,1)
