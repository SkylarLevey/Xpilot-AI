import libpyAI as ai
import math
from random import random

def AI_loop():
    turn, thrust = .5,0
    ai.turnLeft(0)
    ai.turnRight(0)
    ai.thrust(0)
    ai.setTurnSpeed(64)
    
    heading = int(ai.selfHeadingDeg())
    tracking = int(ai.selfTrackingDeg())
    trackWall = ai.wallFeeler(500, tracking)
    trackL3 = ai.wallFeeler(500, tracking + 3)
    trackL10 = ai.wallFeeler(500, tracking + 10)
    trackR3 = ai.wallFeeler(500, tracking - 3)
    trackR10 = ai.wallFeeler(500, tracking - 10)

    frontWall = ai.wallFeeler(500, heading)
    frontL = ai.wallFeeler(500, heading + 15)
    frontR = ai.wallFeeler(500, heading - 15)
    leftWall = ai.wallFeeler(500, heading+90)
    leftF = ai.wallFeeler(500, heading+65)
    leftB = ai.wallFeeler(500, heading+115)
    rightWall = ai.wallFeeler(500,heading-90)
    rightF = ai.wallFeeler(500,heading-65)
    rightB = ai.wallFeeler(500,heading-115)
    backWall = ai.wallFeeler(500, heading - 180)
    backL = ai.wallFeeler(500, heading - 195)
    backR = ai.wallFeeler(500, heading - 165)
    trackHeadRelative = (tracking-heading)
    speed = ai.selfSpeed()

    def findClosestArea(x): 
        return {
            (frontWall + frontL + leftF) : 1, 
            (leftF + leftWall + leftB) : 2, 
            (leftB + backL + backWall) : 3, 
            (backL + backWall + backR) : 4, 
            (backWall + backR + rightB) : 5, 
            (rightB + rightWall + rightF) : 6,
            (rightF + frontR + frontWall) : 7,
        }[x]


    closestVal = min(frontWall+frontL+leftF, leftF+leftWall+leftB, leftB+backL+backWall, backL+backWall+backR, backWall+backR+rightB, rightB+rightWall+rightF, rightF+frontR+frontWall)
    #Find the closest Wall to our ship
    closestArea = findClosestArea(closestVal)   
    #The wall we are likely to crash into if we continue on our current course
    crashWall = min(trackWall, trackL3, trackL10, trackR3, trackR10) 

	#Rules for turning
    if closestArea == 1:
        ai.setTurnSpeed(64)
        ai.turnRight(1)
        turn = 1
    elif closestArea == 2:
        ai.setTurnSpeed(44)
        ai.turnRight(1)
        turn = .8
    elif closestArea == 3:
        ai.setTurnSpeed(24)
        ai.turnRight(1)
        turn = .6
    elif closestArea == 4:
        pass
    elif closestArea == 5:
        ai.setTurnSpeed(24)
        ai.turnLeft(1)
        turn = .4
    elif closestArea == 6:
        ai.setTurnSpeed(44)
        ai.turnLeft(1)
        turn = .2
    elif closestArea == 7:
        ai.setTurnSpeed(64)
        ai.turnLeft(1)
        turn = 0


	#Rules for thrusting
	#if we are going slow and there isn't a wall in front of us
    if min(frontWall,frontL,frontR) > 100 and speed < 4: 
        ai.thrust(1)
        thrust = 1
	#if we are heading toward a wall and we are not facing it
    elif crashWall < 200 and (ai.angleDiff(heading, tracking) > 120): 
        ai.thrust(1)
        thrust = 1
	#If there is a wall very close behind us, get away from it            
    elif backWall < 20 or backL < 20 or backR < 20: 
        ai.thrust(1)
        thrust = 1


ai.start(AI_loop,["-name","Sem2bot","-join","localhost"])  