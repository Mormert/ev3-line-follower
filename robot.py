#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.button import *
from ev3dev2.sensor.lego import *
from time   import time, sleep
#from ev3dev2.motor import SpeedRPM

btn = Button() # will use any button to stop script

# Connect EV3 color sensor.
cl = ColorSensor() 

# Put the color sensor into COL-REFLECT mode
# to measure reflected light intensity.
cl.mode='COL-REFLECT'

# Attach large motors to ports B and C
mB = LargeMotor(OUTPUT_A)
mC = LargeMotor(OUTPUT_B)

motors = MoveTank(OUTPUT_A, OUTPUT_B)

while not btn.any():    # avbryt loopen om en knapp trycks.
    refRead = cl.value()


    if cl.value()<25: # om vi är på svart, så kör rakt fram!
        mB.run_forever(speed_sp=250)
        mC.run_forever(speed_sp=250)
    else: # om vi inte är på vitt, så ska vi skanna

        for i in range(10):
            motors.on_for_seconds(SpeedPercent(-20), SpeedPercent(20), 0.1)
            if(cl.value()<25):
                break

        for i in range(10):
            motors.on_for_seconds(SpeedPercent(20), SpeedPercent(-20), 0.1)
            if(cl.value()<25):
                break

        #break

       
      
mB.stop(stop_action='brake')
mC.stop(stop_action='brake')
mB.run_forever(speed_sp=0)
mC.run_forever(speed_sp=0)