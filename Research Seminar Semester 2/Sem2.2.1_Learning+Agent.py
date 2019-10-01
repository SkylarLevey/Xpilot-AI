#test one on GA Boi.py
#./xpilots -map maps/simple.xp -noQuit -switchBase 1 -fps 32 -map maps/lifeless.xp
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

    outfile = open("Sem2W_1.txt","w")
    outfile.write(str(weight))
    outfile.close()

def getSendData(turn,thrust):
    #Metadata
    heading = int(ai.selfHeadingDeg())
    tracking = int(ai.selfTrackingDeg())
    trackHeadRelative = (tracking-heading)/360
    speed = ai.selfSpeed()/10
    #Wall Feelers
    trackWall = ai.wallFeeler(500, tracking)
    trackL10 = ai.wallFeeler(500, tracking + 10)
    trackR10 = ai.wallFeeler(500, tracking - 10)
    frontWall = ai.wallFeeler(500, heading)
    frontL = ai.wallFeeler(500, heading + 10)
    frontR = ai.wallFeeler(500, heading - 10)
    leftWall = ai.wallFeeler(500, heading+90)
    rightWall = ai.wallFeeler(500,heading-90)
    backWall = ai.wallFeeler(500, heading - 180)
    
    data = [heading/360,tracking/360,trackHeadRelative,speed]
    for i in [trackWall,trackL10,trackR10,frontWall,frontL,frontR,leftWall,rightWall,backWall]:
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

    print(inputs)
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
            frontWall : 1, frontL : 2, 
            leftF : 3, leftWall : 4, leftB : 5,
			backL : 6, backWall : 7, backR : 8,
            rightB : 9, rightWall : 10, rightF : 11,
            frontR : 12
        }[x]

    closestVal = min(frontWall,frontL,leftF,leftWall,leftB,backL,backWall,backR,rightB,rightWall,rightF,frontR)
    #Find the closest Wall to our ship
    closestWall = findClosestArea(closestVal)   
    #The wall we are likely to crash into if we continue on our current course
    crashWall = min(trackWall, trackL3, trackL10, trackR3, trackR10) 

	#Rules for turning
    if closestWall == 1:
        ai.setTurnSpeed(64)
        ai.turnLeft(1)
        turn = 0
    elif closestWall == 2:
        ai.setTurnSpeed(64)
        ai.turnRight(1)
        turn = 1
    elif closestWall == 3:
        ai.setTurnSpeed(52)
        ai.turnRight(1)
        turn = .9
    elif closestWall == 4:
        ai.setTurnSpeed(40)
        ai.turnRight(1)
        turn = .8
    elif closestWall == 5:
        ai.setTurnSpeed(28)
        ai.turnRight(1)
        turn = .7
    elif closestWall == 6:
        ai.setTurnSpeed(16)
        ai.turnRight(1)
        turn = .6
    elif closestWall == 7:
        pass
    elif closestWall == 8:
        ai.setTurnSpeed(16)
        ai.turnLeft(1)
        turn = .4
    elif closestWall == 9:
        ai.setTurnSpeed(28)
        ai.turnLeft(1)
        turn = .3
    elif closestWall == 10:
        ai.setTurnSpeed(40)
        ai.turnLeft(1)
        turn = .2
    elif closestWall == 11:
        ai.setTurnSpeed(52)
        ai.turnLeft(1)
        turn = .1
    elif closestWall == 12:
        ai.setTurnSpeed(64)
        ai.turnLeft(1)
        turn = 0

	#Rules for thrusting
	#if we are going slow and there isn't a wall in front of us
    if min(frontWall,frontL,frontR) > 100 and speed < 3: 
        ai.thrust(1)
        thrust = 1
	#if we are heading toward a wall and we are not facing it
    elif crashWall < 150 and (ai.angleDiff(heading, tracking) > 90): 
        ai.thrust(1)
        thrust = 1
	#If there is a wall very close behind us, get away from it            
    elif backWall < 20 or backL < 20 or backR < 20: 
        ai.thrust(1)
        thrust = 1

    doBackPropigation = True
    if ai.selfAlive() and doBackPropigation:
    #adjust the the learning NN
        infile = open("Sem2W_1.txt","r")
        weight = eval(infile.read())
        infile.close()

        sendData = getSendData(turn, thrust)
        weight = adjustNN(sendData, 13, 6, 2,  weight)

        outfile = open("Sem2W_1.txt","w")
        outfile.write(str(weight))
        outfile.close()

#makeRandomNN(13,6,2)
ai.start(AI_loop,["-name","Sem2","-join","localhost"])  





