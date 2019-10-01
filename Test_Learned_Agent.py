import libpyAI as ai
import math
from random import random

def getSendData():
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
    backL = ai.wallFeeler(500, heading - 200)
    backR = ai.wallFeeler(500, heading - 160)
    
    data = [trackHeadRelative,speed]
    for i in [trackWall,frontL,frontR,leftF,leftB,rightF,rightB,backL,backR]:
        if i == -1:
            data.append(0)
        else:
            data.append(1 - i/500)
    return data

def getOutput(inputs, inputLayerNodeCount, innerLayerNodeCount, outputLayerNodeCount, weight):
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

    #recurrence part 2
    midNode = innerNodeOutput[0]

    return outputNodeOutput

def squash(inputSum):
	return 1/(1+math.exp(-inputSum))

def AI_loop():
    #Release keys
    ai.thrust(0)
    ai.turnLeft(0)
    ai.turnRight(0)
    ai.setTurnSpeed(45)

    sendData = getSendData()
    
    output = getOutput(sendData, 12, 5, 2, weight)
    
    turn, thrust = "N", "N"

    if output[0] >= .55:
        ai.turnRight(1)
        turn = "R"
    elif output[0] < .45:
        ai.turnLeft(1)
        turn = "L"
    ai.setTurnSpeed(abs(output[0]-.5)*100)

    if output[1] > random():
        ai.thrust(1)
        thrust = "Y"

    if ai.selfAlive():
        print (turn +"  "+ str(round(output[0],3)) +"  |  "+ thrust +"  "+ str(round(output[1],3)))


	
infile = open("weights.txt","r")
weight = eval(infile.read())
infile.close()
midNode = 0
ai.start(AI_loop,["-name","bob","-join","localhost"])  






