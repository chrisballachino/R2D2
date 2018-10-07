#!/usr/bin/python

from evdev import InputDevice, categorize, ecodes

#https://core-electronics.com.au/tutorials/using-usb-and-bluetooth-controllers-with-python.html

#creates object gamepad to store the data
gamepad = InputDevice("/dev/input/event3")

print(gamepad)

buttons = {'square':304,
'circle':306,
'x':305,
'triangle':307,
'r_joystick':315,
'l_joystick':314,
'share':312,
'options':313,
'trackpad':317,
'r1':309,
'r2':311,
'l1':308,
'l2':310}

for event in gamepad.read_loop():
   #print(categorize(event))
   if(event.type == ecodes.EV_KEY):
      #print(categorize(event))
      print(event)
   elif(event.type == ecodes.EV_ABS):
      #constantly scrolls
      pass
      #print(event)
   elif(event.type == ecodes.EV_CNT):
      print(event)
