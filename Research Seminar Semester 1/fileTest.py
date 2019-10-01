#test one on GA Boi.py
import libpyAI as ai
import math
from random import random

def makeRandomNN(inputCount, innerLayerNodeCount, outputLayerNodeCount):
    #generates random weights to start
    weight = []
    #inner layer weights
    for j in range(innerLayerNodeCount):
        nodeWeights = []
        for i in range(inputCount+1):
            nodeWeights.append(random()*2-1)
        weight.append(nodeWeights)

    #output layer weights
    for j in range(outputLayerNodeCount):
        nodeWeights = []
        for i in range(innerLayerNodeCount+1):
            nodeWeights.append(random()*2-1)
        weight.append(nodeWeights)

    outfile = open("myBotWeights.txt","w")
    outfile.write(str(weight))
    outfile.close()

def getSendData(turn,thrust,shoot):
    #make all the feelers/get current sichuation data
    heading = int(ai.selfHeadingDeg())
    tracking = int(ai.selfTrackingDeg())
    trackHeadRelative = (tracking-heading)/360

    trackWall = ai.wallFeeler(500, tracking)
    trackL3 = ai.wallFeeler(500, tracking + 3)
    trackL10 = ai.wallFeeler(500, tracking + 10)
    trackR3 = ai.wallFeeler(500, tracking - 3)
    trackR10 = ai.wallFeeler(500, tracking - 10)

    frontWall = ai.wallFeeler(500, heading)
    frontL = ai.wallFeeler(500, heading + 10)
    frontR = ai.wallFeeler(500, heading - 10)

    leftWall = ai.wallFeeler(500, heading+90)

    rightWall = ai.wallFeeler(500,heading-90)

    backWall = ai.wallFeeler(500, heading - 180)
    backL = ai.wallFeeler(500, heading - 185)
    backR = ai.wallFeeler(500, heading - 175)

    speed = ai.selfSpeed()/10

    #get position to enemy
    enemyX = ai.screenEnemyX(0)
    enemyY = ai.screenEnemyY(0)
    selfX = ai.selfX()
    selfY = ai.selfY()
    enemyDegrees = (heading - (math.degrees(math.atan2(enemyY-selfY,enemyX-selfX))+360)%360)/360
    #enemyDegrees = heading - math.degrees(math.atan2(enemyY-selfY,enemyX-selfX))-360
    enemySpeed =  ai.enemySpeed(0)/10
    enemyMoveDirection =  ai.enemyTrackingDeg(0)
    distanceToEnemy = 1 - math.sqrt((selfX-enemyX)**2 + (selfY-enemyY)**2)/500
    relativeTracking = (tracking-180)/360-(enemyMoveDirection-180)/360

    #get shots at us
    data = [heading/360,tracking/360,trackHeadRelative,speed]
    for i in [trackWall,trackL3,trackL10,trackR3,trackR10,frontWall,frontL,frontR,leftWall,rightWall,backWall,backL,backR]:
        if i == -1:
            data.append(0)
        else:
            data.append(1 - i/500)

    for j in [enemySpeed,enemyDegrees,relativeTracking,distanceToEnemy]:
        if not math.isnan(j):
            if enemyX == -1:
                data.append(0)
            else:
                data.append(j)
        else:
            data.append(0)
    for k in [turn,thrust,shoot]:
        data.append(k)

    #print("distToEnemy",data[20]*500,"relTrack",data[19]*360)
    return data

def squash(inputSum):
    return 1/(1+math.exp(-inputSum))

def adjustNN(inputs, inputLayerNodeCount, innerLayerNodeCount, outputLayerNodeCount, weight):
    innerNodeOutput = []
    for i in range(innerLayerNodeCount):
        innerNodeOutput.append(0)
    outputNodeOutput = []
    for j in range(outputLayerNodeCount):
         outputNodeOutput.append(0)

    #calculate our neural net's outputs

    #for each node in the hidden layer
    for innerNode in range(innerLayerNodeCount):
        innerSum = 0
        #sum up all inputs * their given weights
        for inputValue in range(inputLayerNodeCount):
            innerSum += inputs[inputValue]*weight[innerNode][inputValue]
        #record the output in a list
        innerNodeOutput[innerNode] = squash(innerSum - weight[innerNode][inputLayerNodeCount])
    #for each node in the output layer
    for outputNode in range(outputLayerNodeCount):
        outputSum = 0
        #sum up all inputs * their given weights
        for innerNodeOpt in range(innerLayerNodeCount):
            outputSum += innerNodeOutput[innerNodeOpt]*weight[innerLayerNodeCount+outputNode][innerNodeOpt]
        #record the output in a list
        outputNodeOutput[outputNode] = squash(outputSum - weight[innerLayerNodeCount+outputNode][innerLayerNodeCount])

    #get the desired outputs
    desiredOutput = inputs[len(inputs)-outputLayerNodeCount:]

    #print(inputs)
    #back propigation
    
    learningConstant = .4
    #output node weights
    for outputNode in range(outputLayerNodeCount):
        #adjusts each weight from the inner to ouput layer
        for w in range(innerLayerNodeCount):
            weight[innerLayerNodeCount+outputNode][w] -= \
                learningConstant * \
                innerNodeOutput[w] * \
                outputNodeOutput[outputNode] * (1-outputNodeOutput[outputNode]) * \
                (outputNodeOutput[outputNode] - desiredOutput[outputNode])
        #adjusts the threshhold of each output node
        weight[innerLayerNodeCount+outputNode][innerLayerNodeCount] -= \
            learningConstant * -1 * \
            outputNodeOutput[outputNode] * (1-outputNodeOutput[outputNode]) * \
            (outputNodeOutput[outputNode] - desiredOutput[outputNode])

    #middle layer node weights
    for node in range(innerLayerNodeCount):
        #calulate the effect this inner node had on the total output
        errorSum = 0
        for outputNode in range(outputLayerNodeCount):
            errorSum += \
                outputNodeOutput[outputNode] * (1-outputNodeOutput[outputNode]) * \
                (outputNodeOutput[outputNode] - desiredOutput[outputNode]) * \
                weight[innerLayerNodeCount+outputNode][outputNode]
        #adjusts each weight from the input to inner layer
        for w in range(inputLayerNodeCount):
            #adjust the weight
            weight[node][w] -= \
                learningConstant * \
                inputs[w] * \
                innerNodeOutput[node] * (1-innerNodeOutput[node]) * \
                errorSum
        #adjusts the threshhold of each inner node
        weight[node][inputLayerNodeCount] -= \
            learningConstant * -1 * \
            innerNodeOutput[node] * (1-innerNodeOutput[node]) * \
			errorSum

    #calc error for graph
    er = 0
    for i in range(len(desiredOutput)):
        er += .5*(desiredOutput[i] - outputNodeOutput[i])**2
    global numFrames,totalError
    totalError += er
    numFrames += 1
    if numFrames >= 500:
        graphInfo = open("graphStuff.txt","r")
        graphList = graphInfo.read()
        graphInfo.close()
        graphList += str(totalError/numFrames) + "\n"
        print(graphList)
        graphWrite = open("graphStuff.txt","w")
        graphWrite.write(str(graphList))
        graphWrite.close()
        totalError = 0
        numFrames = 0
    
    return weight

def AI_loop():
    #Release keys
    ai.thrust(0)
    ai.turnLeft(0)
    ai.turnRight(0)
    ai.setTurnSpeed(45)
    turn, thrust, shoot = 0.5, 0, 0
    maxSpeed = 3
    shotAngle = 9
    wallClose = 12
    #Set variables"""
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
    
    #Code for finding the angle to the closest ship
    targetX,  targetY = ai.screenEnemyX(0), ai.screenEnemyY(0)
    calcDir = 0

    if targetX- ai.selfX() != 0:
        calcDir = (math.degrees(math.atan2((targetY - ai.selfY()), (targetX- ai.selfX()))) + 360)%360
    crashWall = min(trackWall,  trackLWall,  trackRWall) #The wall we are likely to crash into if we continue on our current course

    #Rules for turning
    if crashWall > wallClose*speed and closest > 25 and targetX != -1:  #If we are far enough away from a predicted crash and no closer than 25 pixels to a wall we can try and aim and kill them
        diff = (calcDir - heading)
        if ai.shotAlert(0) > -1 and ai.shotAlert(0) < 35:   #If we are about to get shot
            ai.turnRight(1)  #Screw aiming and turn right and thrust
            ai.thrust(1)
            thrust = 1
            #This is arguably a horrible strategy because our sideways profile is much larger, but it's required for the grade
        elif diff >= 0:
            if diff >= 180:
                ai.turnRight(1)     #If the target is to our right- turn right
                turn = 1
            else :                       
                ai.turnLeft(1)      #If the target is to our left - turn left
                turn = 0
        else :
            if diff > -180:
                ai.turnRight(1)     #If the target is to our right - turn right
                turn = 1
            else :
                ai.turnLeft(1)      #If the target is to our left - turn left
                turn = 0
    #Rules for avoiding death      
    else :
        # if crashWall/ai.selfSpeed() > ai.closestShot() :
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

    if abs(calcDir - heading) < shotAngle : #If we are close to the current proper trajectory for a shot then fire
        ai.fireShot()
        shoot = 1


    #adjust the the learning NN
    infile = open("myBotWeights.txt","r")
    weight = eval(infile.read())
    infile.close()

    sendData = getSendData(turn, thrust, shoot)
    weight = adjustNN(sendData, 21, 8, 3,  weight)

    outfile = open("myBotWeights.txt","w")
    outfile.write(str(weight))
    outfile.close()

#makeRandomNN(21,8,3)

numFrames, totalError = 0, 0
ai.start(AI_loop,["-name","fileTest","-join","localhost"])  



