# Released by rdb under the Unlicense (unlicense.org)
# Based on information from:
# https://www.kernel.org/doc/Documentation/input/joystick-api.txt

import os, struct, array
from fcntl import ioctl

# We'll store the states here.
axis_states = {}
button_states = {}

# These constants were borrowed from linux/input.h
axis_names = {
    0x00 : 'x',
    0x01 : 'y',
    0x02 : 'z',
    0x03 : 'l2_gradual',
    0x04 : 'r2_gradual',
    0x05 : 'rz',
    0x06 : 'trottle',
    0x07 : 'rudder',
    0x08 : 'wheel',
    0x09 : 'gas',
    0x0a : 'brake',
    0x10 : 'hat0x',
    0x11 : 'hat0y',
    0x12 : 'hat1x',
    0x13 : 'hat1y',
    0x14 : 'hat2x',
    0x15 : 'hat2y',
    0x16 : 'hat3x',
    0x17 : 'hat3y',
    0x18 : 'pressure',
    0x19 : 'distance',
    0x1a : 'tilt_x',
    0x1b : 'tilt_y',
    0x1c : 'tool_width',
    0x20 : 'volume',
    0x28 : 'misc',
}

button_names = {
    0x120 : 'trigger',
    0x121 : 'thumb',
    0x122 : 'thumb2',
    0x123 : 'top',
    0x124 : 'top2',
    0x125 : 'pinkie',
    0x126 : 'base',
    0x127 : 'base2',
    0x128 : 'base3',
    0x129 : 'base4',
    0x12a : 'base5',
    0x12b : 'base6',
    0x12f : 'dead',
    0x130 : 'square',
    0x131 : 'x',
    0x132 : 'circle',
    0x133 : 'triangle',
    0x134 : 'l1',
    0x135 : 'r1',
    0x136 : 'l2',
    0x137 : 'r2',
    0x138 : 'share',
    0x139 : 'options',
    0x13a : 'select',
    0x13b : 'start',
    0x13c : 'mode',
    0x13d : 'thumbl',
    0x13e : 'thumbr',

    0x220 : 'dpad_up',
    0x221 : 'dpad_down',
    0x222 : 'dpad_left',
    0x223 : 'dpad_right',

    # XBox 360 controller uses these codes.
    0x2c0 : 'dpad_left',
    0x2c1 : 'dpad_right',
    0x2c2 : 'dpad_up',
    0x2c3 : 'dpad_down',
}

axis_map = []
button_map = []

class ps4_controller:
    def __init__(self, input):
        # Open the joystick device.
        self.fn = input
        self.jsdev = open(self.fn, 'rb')

        # Get the device name.
        #buf = bytearray(63)
        self.buf = array.array('c', ['\0'] * 64)
        ioctl(self.jsdev, 0x80006a13 + (0x10000 * len(self.buf)), self.buf) # JSIOCGNAME(len)
        self.js_name = self.buf.tostring()
        
        # Get number of axes and buttons.
        self.buf = array.array('B', [0])
        ioctl(self.jsdev, 0x80016a11, self.buf) # JSIOCGAXES
        self.num_axes = self.buf[0]

        self.buf = array.array('B', [0])
        ioctl(self.jsdev, 0x80016a12, self.buf) # JSIOCGBUTTONS
        self.num_buttons = self.buf[0]

        # Get the axis map.
        self.buf = array.array('B', [0] * 0x40)
        ioctl(self.jsdev, 0x80406a32, self.buf) # JSIOCGAXMAP

        for self.axis in self.buf[:self.num_axes]:
            self.axis_name = axis_names.get(self.axis, 'unknown(0x%02x)' % self.axis)
            axis_map.append(self.axis_name)
            axis_states[self.axis_name] = 0.0

        # Get the button map.
        self.buf = array.array('H', [0] * 200)
        ioctl(self.jsdev, 0x80406a34, self.buf) # JSIOCGBTNMAP

        for self.btn in self.buf[:self.num_buttons]:
            self.btn_name = button_names.get(self.btn, 'unknown(0x%03x)' % self.btn)
            button_map.append(self.btn_name)
            button_states[self.btn_name] = 0
        
        self.xcounter = 0
        self.ycounter = 0
        self.max_counter = 50
        self.last_x_val = 0
        self.last_y_val = 0
        self.last_z_val = 0
        self.last_rz_val = 0
        self.left_stick_change = False
        self.right_stick_change = False

    #blocking call - reads from std input
    def read(self):
        evbuf = self.jsdev.read(8)
        if evbuf:
            time, value, type, number = struct.unpack('IhBB', evbuf)

            if type & 0x80:
                 return ('null',0)

            if type & 0x01:
                button = button_map[number]
                if button:
                    button_states[button] = value
                    if value:
                        return (button,1)
                        #print "%s pressed" % (button)
                    else:
                        return (button,0)
                        #print "%s released" % (button)

            if type & 0x02:
                    axis = axis_map[number]
                    if axis:
                        fvalue = value / 32767.0
                        if axis == 'x':
                            self.last_x_val = fvalue
                            self.left_stick_change = True
                        elif axis == 'y':
                            self.last_y_val = fvalue
                            self.left_stick_change = True
                        elif axis == 'z':
                            self.last_z_val = fvalue
                            self.right_stick_change = True
                        elif axis == 'rz':
                            self.last_rz_val = fvalue
                            self.right_stick_change = True

                        if(self.left_stick_change):
                            #print('(%.3f, %.3f)'%(self.last_x_val,self.last_y_val))                            
                            self.left_stick_change = False
                            return (('ly',self.last_y_val),('lx',self.last_x_val))
                        if(self.right_stick_change):
                            #print('(%.3f, %.3f)'%(self.last_z_val,self.last_rz_val))
                            self.right_stick_change = False
                            return (('ry',self.last_rz_val),('rx',self.last_z_val))

if __name__=='__main__':
    c = ps4_controller('/dev/input/js0')
    while(True):
        (keyType,keyVal) = c.read()
        
        
