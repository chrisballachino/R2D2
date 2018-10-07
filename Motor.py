#!/usr/bin/python

import RPi.GPIO as GPIO
import time

#TODO pick pins for motors two and three
pwm_pins = [19,12]
dr_pins = [27,21]

class Motor:
    def __init__(self,number):
        self.motor_num = number
        self.current_direction = -1
        self.speed = 0

    def init(self):
        GPIO.setup(pwm_pins[self.motor_num],GPIO.OUT)
        GPIO.setup(dr_pins[self.motor_num],GPIO.OUT)
        #self.pwm = GPIO.PWM(pwm_pins[self.motor_num],100000)
        self.pwm = GPIO.PWM(pwm_pins[self.motor_num],100)
        self.pwm.ChangeDutyCycle(0)

    #speed is between 0 and 100
    #direction is 1 for forward, 0 for backwards
    def set_speed(self,speed,direction):
        if(speed == self.speed):
            return #do nothing
        self.speed = speed
        if(direction==1):
            GPIO.output(pwm_pins[self.motor_num],GPIO.HIGH)
        else:
            GPIO.output(pwm_pins[self.motor_num],GPIO.LOW)
        if(self.current_direction != direction):
            self.current_direction = direction
        #self.engage_motor(False)
        #self.pwm.stop()
        self.pwm.ChangeDutyCycle(speed)
        #print(self.pwm)
        #if(speed != 0):
        #    self.pwm.start(speed)
        #self.engage_motor(True)

    def engage_motor(self,run):
        if(run):
            self.pwm.start(self.speed)
        else:
            self.pwm.stop()
if __name__=='__main__':
    GPIO.setmode(GPIO.BCM)
    m = Motor(0)
    m.init()

    print('Forward slow')
    m.engage_motor(False)
    m.set_speed(25,1)
    m.engage_motor(True)
    time.sleep(5)

    print('Forward medium')
    m.set_speed(50,1)
    time.sleep(5)

    print('Forward fast')
    m.set_speed(75,1)
    time.sleep(5)

    print('Forward reeeally fast')
    m.set_speed(95,1)
    time.sleep(5)

    print('Stopping')
    m.engage_motor(False)
