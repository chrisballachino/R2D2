#!/usr/bin/python

import RPi.GPIO as GPIO
import time

  
def simple_blink(pin):
  #GPIO.setmode(GPIO.BCM)
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(pin,GPIO.OUT)

  while True:
    print("GPIO Low")
    GPIO.output(pin,GPIO.LOW)
    time.sleep(10)
    print("GPIO High")
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(10)

def simple_pwm():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(21,GPIO.OUT)
  pwm = GPIO.PWM(21,100000)
  pwm.ChangeDutyCycle(50)
  pwm.start(1) 
  time.sleep(10)
  pwm.stop() 

def drok_pwm():
  GPIO.setmode(GPIO.BCM)
 
  GPIO.setup(19,GPIO.OUT)
  GPIO.setup(27,GPIO.OUT)
  GPIO.output(27,GPIO.HIGH)
  pwm = GPIO.PWM(19,100000)
  pwm.ChangeDutyCycle(50)
  pwm.start(1)
  time.sleep(5)
  pwm.stop()
  time.sleep(1)
  GPIO.output(27,GPIO.LOW)
  time.sleep(1)
  pwm.start(1)
  time.sleep(5)
  #GPIO.output(13,1)
  #time.sleep(1)
  #print(GPIO.input(5))
  #time.sleep(1)
  #GPIO.output(13,0)
  #time.sleep(1)
  #print(GPIO.input(5))
  #time.sleep(1)
  pwm.stop()

def check_pwm():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(6,GPIO.OUT)
  GPIO.setup(13,GPIO.OUT)
  GPIO.setup(19,GPIO.OUT)
  GPIO.setup(26,GPIO.OUT)


  while true:
    print("Motor forward")
    GPIO.output(6,GPIO.HIGH)
    GPIO.output(13,GPIO.LOW)
    GPIO.output(19,GPIO.HIGH)
    GPIO.output(26,GPIO.LOW)
    time.sleep(10)
    print("Motor backward")
    GPIO.output(6,GPIO.LOW)
    GPIO.output(13,GPIO.HIGH)
    GPIO.output(19,GPIO.LOW)
    GPIO.output(26,GPIO.HIGH)
    time.sleep(10)


if __name__=='__main__':
  #simple_pwm()
  #simple_blink(3)
  drok_pwm()
  GPIO.cleanup()
