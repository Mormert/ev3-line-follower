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

timings = 0.5

motors = MoveTank(OUTPUT_A, OUTPUT_B)

def main():
    try:
        while not btn.any():    # avbryt loopen om en knapp trycks.

            if cl.value()<25:   # om vi är på svart, så kör rakt fram!
                mB.run_forever(speed_sp=600)
                mC.run_forever(speed_sp=600)
                #motors.run_forever(SpeedPercent(20), SpeedPercent(20))
                print("Is on black line")
            else: # om vi inte är på vitt, så ska vi skanna

                blackFound = False

                blackFound = searchForBlackLine(-20,20,timings, blackFound)
                if blackFound == False:
                    print("Turning left")
                blackFound = searchForBlackLine(20,-20,timings*2, blackFound)
                if blackFound == False:
                    print("Turning right")
                blackFound = searchForBlackLine(-20,20,timings, blackFound)
                if blackFound == False:
                    print("Going back to ")

                while blackFound == False:
                    print("Going forward to try and find black line...")
                    blackFound = searchForBlackLine(40,40,timings*0.5, blackFound)
                    blackFound = searchForBlackLine(-20,20,timings, blackFound)
                    blackFound = searchForBlackLine(20,-20,timings*2, blackFound)
                    blackFound = searchForBlackLine(-20,20,timings, blackFound)

    except Exception as e: print(e)
        
       

def searchForBlackLine(motor1, motor2, timeSeconds, bf):
    if bf == False:
        motors.on_for_seconds(SpeedPercent(motor1), SpeedPercent(motor2), timeSeconds*2, block=False)
        for i in range(int(100 * timeSeconds)): # skanna 100 ggr
            if(cl.value()<25): # om vi hittar svart igen
                return True
            sleep(0.01) # skanna var 10 ms
        return False
    else:
        return True
      
def goAroundObstacle():

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

main()

#try:
 #   motors.stop(stop_action='brake')
  #  motors.run_forever(SpeedPercent(0), SpeedPercent(0))
#except Exception as e: print(e)

mB.stop(stop_action='brake')
mC.stop(stop_action='brake')
mB.run_forever(speed_sp=0)
mC.run_forever(speed_sp=0)