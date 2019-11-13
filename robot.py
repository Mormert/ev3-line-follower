#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.button import *
from ev3dev2.sensor.lego import *
from time   import time, sleep

# en knapp för att kunna stänga av programmet
btn = Button() 

# referens ljussensorn-objektet
cl = ColorSensor() 

# vi kör på "reflect" mode. Under cirka 6-7 i value anser vi som svart linje.
cl.mode='COL-REFLECT'

# referens till US-sensorn-objektet
us = UltrasonicSensor()
# US-sensorn kör i CM (men egentligen mm!)
us.mode = 'US-DIST-CM'


motorA = LargeMotor(OUTPUT_A)   # vi vill ha kontroll över motor A
motorB = LargeMotor(OUTPUT_B)   # vi vill ha kontroll över motor A

timings = 0.5                   # en konstant variabel som anger hur länge vi ska söka efter svarta linjen

# vi vill också ha enkel kontroll över båda motorerna samtidigt.
motors = MoveTank(OUTPUT_A, OUTPUT_B)

def main():
    try:
        while not btn.any():        # avbryt loopen om en knapp trycks.

            if us.value() < 100:    # om ett objekt är 10 cm från US-sensorn
                goAroundObstacle()  # gå runt objektet

            if cl.value()<25:   # om vi är på svart, så kör rakt fram!
                motorA.run_forever(speed_sp=200) # en godtycklig hastighet
                motorB.run_forever(speed_sp=200) # på båda motorerna
            else: # om vi inte är på vitt, så ska vi gå in i "scan-mode"

                blackFound = False

                # vi har en bool blackFound, som blir True i funktionen searchForBlackLine
                # om ljussensorn känner av svart färg. searchForBlackLine-funktionen
                # körs tills den är klar, för att sedan köras igen, fast med andra argument.

                blackFound = searchForBlackLine(-20,20,timings, blackFound)

                blackFound = searchForBlackLine(20,-20,timings*2, blackFound)

                blackFound = searchForBlackLine(-20,20,timings, blackFound)


                # så länge vi inte hittat svart färg så vill vi sakta gå fram
                # och skanna av miljön, åt vänster, åt höger. Så snart vi hittar
                # svart igen, så går vi tillbaka till att åka rakt fram på svarta linjen.
                while blackFound == False:
                    blackFound = searchForBlackLine(20,20,timings*0.5, blackFound)
                    blackFound = searchForBlackLine(-20,20,timings, blackFound)
                    blackFound = searchForBlackLine(20,-20,timings*2, blackFound)
                    blackFound = searchForBlackLine(-20,20,timings, blackFound)

    except Exception as e: print(e)
    # det är bra att ha en exception-handler,
    # för annars fortsätter programmet köra
    # och man måste reboota EV3-roboten.
        
       

def searchForBlackLine(motor1, motor2, timeSeconds, bf):
    if bf == False:
        motors.on_for_seconds(SpeedPercent(motor1), SpeedPercent(motor2), timeSeconds*2, block=False)
        for i in range(int(100 * timeSeconds)): # skanna 100 ggr
            if us.value() < 100:                # om ett objekt är 10 cm från US-sensorn

                goAroundObstacle()              # gå runt objektet
                return False                    # vi måste returnera något för att komma ur denna funktion.

            if(cl.value()<25):                  # om vi hittar svart igen
                return True
            sleep(0.01)                         # skanna var 10 ms
        return False
    else:
        return True
      
def goAroundObstacle():                         # en hårdkodad funtkion för att gå runt ett objekt

    turn90DegreeLeft(0.3)
    goStraight(0.7)
    turn90DegreeRight(0.3)
    goStraight(0.5)
    turn90DegreeRight()

    goUntil = False
    while goUntil == False:                     # vi kör tills vi hittar tillbaka till den svarta linjen.
        goUntil = searchForBlackLine(50,50,1, goUntil)

    turn90DegreeLeft()                          # när vi hittat svarta linjen igen gör vi en 90-graders-sväng igen.



def turn90DegreeLeft(goforsec):
    motors.on_for_seconds(SpeedPercent(-50), SpeedPercent(50), goforsec)

def turn90DegreeRight(goforsec):
    motors.on_for_seconds(SpeedPercent(50), SpeedPercent(-50), goforsec)

def goStraight(goforsec):
    motors.on_for_seconds(SpeedPercent(50), SpeedPercent(50), goforsec)

main()

#   vi stänger av motorerna i slutet på programmet.
motorA.stop(stop_action='brake')
motorB.stop(stop_action='brake')
motorA.run_forever(speed_sp=0)
motorB.run_forever(speed_sp=0)

#   Johan Lind, 2019 Örebro universitet
#   GNU GENERAL PUBLIC LICENSE