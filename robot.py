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

        blackFound = searchForBlackLine(-20,20,1, blackFound)
        blackFound = searchForBlackLine(20,-20,2, blackFound)
        blackFound = searchForBlackLine(-20,20,1, blackFound)

        while blackFound == False:
            blackFound = searchForBlackLine(20,20,1, blackFound)
       

def searchForBlackLine(motor1, motor2, timeSeconds, bf):
    if bf == False:
        motors.on_for_seconds(SpeedPercent(motor1), SpeedPercent(motor1, timeSeconds, block=False))
            for i in range(100 * timeSeconds): # skanna 100 ggr
                if(cl.value()<25): # om vi hittar svart igen
                    return True
                sleep(0.01) # skanna var 10 ms
        return False
    else:
        return True
      
def goAroundObstacle:

    turn90DegreeLeft()
    goStraight()
    turn90DegreeRight()
    goStraight()
    turn90DegreeRight()

    goUntil = False
    while goUntil == False:
        goUntil = searchForBlackLine(10,10,1, goUntil)

    turn90DegreeLeft()



def turn90DegreeLeft():
    #motors.on_for_seconds(SpeedPercent(50), SpeedPercent(-50), 1)
    motors.on_for_rotations(SpeedPercent(-50), SpeedPercent(50), 3)

def turn90DegreeRight():
    #motors.on_for_seconds(SpeedPercent(-50), SpeedPercent(50), 1)
    motors.on_for_rotations(SpeedPercent(50), SpeedPercent(-50), 3)

def goStraight():
    motors.on_for_seconds(SpeedPercent(50), SpeedPercent(50), 5)

mB.stop(stop_action='brake')
mC.stop(stop_action='brake')
mB.run_forever(speed_sp=0)
mC.run_forever(speed_sp=0)