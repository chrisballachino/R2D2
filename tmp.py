from evdev import InputDevice, categorize, ecodes

for ecode in dir(ecodes):
   print(ecode)
