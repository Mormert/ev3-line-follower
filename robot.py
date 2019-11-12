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

    if cl.value()<25: # om vi är på svart, så kör rakt fram!
        mB.run_forever(speed_sp=250)
        mC.run_forever(speed_sp=250)
    else: # om vi inte är på vitt, så ska vi skanna

        blackFound = False

        if blackFound == False:
            motors.on_for_seconds(SpeedPercent(-20), SpeedPercent(20, 1, block=False))
            for i in range(100): # skanna 100 ggr
                if(cl.value()<25): # om vi hittar svart igen
                    blackFound = True
                    break
                sleep(0.01) # skanna var 10 ms

        if blackFound == False:
            motors.on_for_seconds(SpeedPercent(20), SpeedPercent(-20, 2, block=False))
            for i in range(200): # skanna 200 ggr fast åt motsatt håll
                if(cl.value()<25): # om vi hittar svart igen
                    blackFound = True
                    break
                sleep(0.01) # skanna var 10 ms

        if blackFound == False:
            motors.on_for_seconds(SpeedPercent(-20), SpeedPercent(20, 1, block=False))
            for i in range(100): # skanna 100 ggr
                if(cl.value()<25): # om vi hittar svart igen
                    blackFound = True
                    break
                sleep(0.01) # skanna var 10 ms

        if blackFound == False: # om svart fortfarande inte hittats, 
                                # antar vi att det är ett glapp och
                                # åker rakt fram tills vi hittar svart igen.
            while(blackFound == False):
                motors.on_for_seconds(SpeedPercent(20), SpeedPercent(20, 1, block=False))
                for i in range(100): # skanna 100 ggr
                    if(cl.value()<25): # om vi hittar svart igen
                        blackFound = True
                        break
                    sleep(0.01) # skanna var 10 ms
       
      
mB.stop(stop_action='brake')
mC.stop(stop_action='brake')
mB.run_forever(speed_sp=0)
mC.run_forever(speed_sp=0)