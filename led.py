#!/usr/bin/python

import RPi.GPIO as GPIO
import time

def simple_blink(pin):
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(pin,GPIO.OUT)

  while True:
    print("GPIO Low")
    GPIO.output(pin,GPIO.LOW)
    time.sleep(2)
    print("GPIO High")
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(2)

if __name__=='__main__':
  simple_blink(17)
