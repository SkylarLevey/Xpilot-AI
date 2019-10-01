#./xpilots -map maps/simple.xp -noQuit -switchBase 1 -fps 32 -map maps/lifeless.xp
import libpyAI as ai
import math
import time
from random import random

def getSendData(turn,thrust):
    #Metadata
    heading = int(ai.selfHeadingDeg())
    tracking = int(ai.selfTrackingDeg())
    trackHeadRelative = ai.angleDiff(heading, tracking)/180
    speed = ai.selfSpeed()/10
    #Wall Feelers
    trackWall = ai.wallFeeler(500, tracking)
    frontL = ai.wallFeeler(500, heading + 10)
    frontR = ai.wallFeeler(500, heading - 10)
    leftF = ai.wallFeeler(500, heading + 70)
    leftB = ai.wallFeeler(500, heading + 110)
    rightF = ai.wallFeeler(500,heading - 70)
    rightB = ai.wallFeeler(500,heading - 110)
    backL = ai.wallFeeler(500, heading - 190)
    backR = ai.wallFeeler(500, heading - 170)
    
    data = [trackHeadRelative,speed]
    for i in [trackWall,frontL,frontR,leftF,leftB,rightF,rightB,backL,backR]:
        if i == -1:
            data.append(0)
        else:
            data.append(1 - i/500)
    for j in [turn,thrust]:
        data.append(j)

    return data


def squash(inputSum):
    return 1/(1+math.exp(-inputSum))

def adjustNN(inputs, inputLayerNodeCount, innerLayerNodeCount, outputLayerNodeCount, weight):
	#recurrence
    global midNode
    inputs.insert(0,midNode)

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

    #recurrence part 2
    midNode = innerNodeOutput[0]

#    print(inputs,time.ctime())
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
    graph = False
    if graph:
        er = 0
        for i in range(len(desiredOutput)):
            er += .5*(desiredOutput[i] - outputNodeOutput[i])**2
        global numFrames,totalError
        totalError += er
        numFrames += 1
        print(numFrames)
        if numFrames >= 500:
            graphInfo = open("graphStuff.txt","r")
            graphList = graphInfo.read()
            graphInfo.close()
            graphList += str(totalError/numFrames) + "\n"
            #print(graphList)
            graphWrite = open("graphStuff.txt","w")
            graphWrite.write(str(graphList))
            graphWrite.close()
            totalError = 0
            numFrames = 0
    
    return weight

def AI_loop():
    turn, thrust = .5,0
    ai.turnLeft(0)
    ai.turnRight(0)
    ai.thrust(0)
    ai.setTurnSpeed(64)
    
    heading = int(ai.selfHeadingDeg())
    tracking = int(ai.selfTrackingDeg())

    trackWall = ai.wallFeeler(500, tracking)

    frontL = ai.wallFeeler(500, heading + 10)
    frontR = ai.wallFeeler(500, heading - 10)
    leftF = ai.wallFeeler(500, heading + 70)
    leftB = ai.wallFeeler(500, heading + 110)
    rightF = ai.wallFeeler(500,heading - 70)
    rightB = ai.wallFeeler(500,heading - 110)
    backL = ai.wallFeeler(500, heading - 190)
    backR = ai.wallFeeler(500, heading - 170)

    speed = ai.selfSpeed()

    def findClosestArea(x): 
        return {
            frontL : 1, leftF : 2, leftB : 3, backL : 4, 
            backR : 5, rightF : 6, rightB : 7, frontR : 8
        }[x]

    closestVal = min(frontL,leftF,leftB,backL,backR,rightF,rightB,frontR)
    #Find the closest Wall to our ship
    closestWall = findClosestArea(closestVal)   

	#Rules for turning
	#if we are heading for a wall, turn away from it
    if trackWall < 100:
	#round(abs(ai.angleDiff(heading, tracking))/3)
        ai.setTurnSpeed(15+round(abs(ai.angleDiff(heading, tracking))/4))
        if ai.angleDiff(heading, tracking) > 0:
            ai.turnRight(1)
            turn = .9
        else:
            ai.turnLeft(1)
            turn = .1
	#otherwise turn away from the closest wall
    elif closestWall == 1:
        ai.setTurnSpeed(64)
        ai.turnRight(1)
        turn = 1
    elif closestWall == 2:
        ai.setTurnSpeed(46)
        ai.turnRight(1)
        turn = .9
    elif closestWall == 3:
        ai.setTurnSpeed(28)
        ai.turnRight(1)
        turn = .8
    elif closestWall == 4:
        ai.setTurnSpeed(10)
        ai.turnRight(1)
        turn = .6
    elif closestWall == 5:
        ai.setTurnSpeed(10)
        ai.turnLeft(1)
        turn = .4
    elif closestWall == 6:
        ai.setTurnSpeed(28)
        ai.turnLeft(1)
        turn = .2
    elif closestWall == 7:
        ai.setTurnSpeed(26)
        ai.turnLeft(1)
        turn = .1
    elif closestWall == 8:
        ai.setTurnSpeed(64)
        ai.turnLeft(1)
        turn = 0

 
    #Rules for thrusting

    #if we are going slow and there isn't a wall in front of us
    if min(frontL,frontR) > 100 and speed < 2.5: 
        ai.thrust(1)
        thrust = 1
    #if we are going too fast and are facing away from the direction we are heading
    elif abs(ai.angleDiff(heading, tracking)) > 135 and speed > 2.5:
        ai.thrust(1)
        thrust = 1

    #if we are heading toward a wall and we are not facing it
    elif trackWall < 150 and (abs(ai.angleDiff(heading, tracking)) > 120): 
        ai.thrust(1)
        thrust = 1
    #If there is a wall very close behind us, get away from it            
    elif backL < 25 or backR < 25: 
        ai.thrust(1)
        thrust = 1

    doBackPropigation = True
    if ai.selfAlive() and doBackPropigation:
    #adjust the the learning NN
        infile = open("weights.txt","r")
        weight = eval(infile.read())
        infile.close()

        sendData = getSendData(turn, thrust)
        weight = adjustNN(sendData, 12, 5, 2,  weight)

        outfile = open("weights.txt","w")
        outfile.write(str(weight))
        outfile.close()

numFrames, totalError = 0, 0
midNode = 0
ai.start(AI_loop,["-name","bob","-join","localhost")  





