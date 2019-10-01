import libpyAI as ai
import math
from random import random

def AI_loop():
    #Release keys
    ai.thrust(0)
    ai.turnLeft(0)
    ai.turnRight(0)
    ai.setTurnSpeed(45)

    turn, thrust = 0.5, 0
    maxSpeed = 3
    shotAngle = 9
    wallClose = 12

    heading = int(ai.selfHeadingDeg())
    tracking = int(ai.selfTrackingDeg())
    trackWall = ai.wallFeeler(500,  tracking)
    trackLWall = ai.wallFeeler(500,  tracking+3)
    trackRWall = ai.wallFeeler(500,  tracking - 3)
    frontWall = ai.wallFeeler(500,heading)
    flWall = ai.wallFeeler(500,  heading + 10)
    frWall = ai.wallFeeler(500,  heading - 10)
    leftWall = ai.wallFeeler(500,heading+90)
    rightWall = ai.wallFeeler(500,heading-90)
    trackWall = ai.wallFeeler(500,tracking)
    backWall = ai.wallFeeler(500, heading - 180)
    backLeftWall = ai.wallFeeler(500,  heading - 185)
    backRightWall = ai.wallFeeler(500,  heading - 175)
    speed = ai.selfSpeed()

    closest = min(frontWall, leftWall, rightWall, backWall,  flWall,  frWall)
    def closestWall(x): #Find the closest Wall
        return {
            frontWall : 1,
            leftWall : 2,
            rightWall : 3,
            backWall : 4,
            flWall : 5,
            frWall : 6,
        }[x]
    wallNum = closestWall(closest)
    
    crashWall = min(trackWall,  trackLWall,  trackRWall) #The wall we are likely to crash into if we continue on our current course
    
    #Rules for turning
    if wallNum == 1 or wallNum == 5 or wallNum == 6:    #Front Wall is Closest (Turn Away From It)
        ai.turnLeft(1)
        turn = 0
    elif wallNum == 2 :  # Left Wall is Closest (Turn Away From It)
        ai.turnRight(1)
        turn = 1
    elif wallNum == 3 :   #Right Wall is Closest (Turn Away From It)
        ai.turnLeft(1)
        turn = 0
    else :                                                      #Back Wall is closest- turn so that we are facing directly away from it
        if backLeftWall < backRightWall:
           ai.turnRight(1)                                  #We need to turn right to face more directly away from it
           turn = 1
        if backLeftWall > backRightWall:        # We need to turn left to face more directly away from it
           ai.turnLeft(1)
           turn = 0

    #Rules for thrusting
    if speed < maxSpeed and frontWall > 100:   #If we are moving slowly and we won't ram into anything, accelerate
        ai.thrust(1)
        thrust = 1
    elif trackWall < 250  and (ai.angleDiff(heading,  tracking) > 120):  #If we are getting close to a wall, and we can thrust away from it, do so
        ai.thrust(1)
        thrust = 1
    elif backWall < 20: #If there is a wall very close behind us, get away from it
        ai.thrust(1)
        thrust = 1


ai.start(AI_loop,["-name","Sem1bot","-join","localhost"])  
