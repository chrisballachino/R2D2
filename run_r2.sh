#!/bin/bash

/home/r2/motor 19 27 7777 &
/home/r2/dome 16 22 7778 &
/home/r2/dome 2 3 7779 &
/home/r2/led_grid &
python /home/r2/r2d2.py 
