#test one on GA Boi.py
#./xpilots -map maps/simple.xp -noQuit -switchBase 1 -fps 32 -map maps/lifeless.xp
import libpyAI as ai
import math
from random import random

def makeRandomNN1(inputCount, innerLayerNodeCount, outputLayerNodeCount):
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

def makeRandomNN2(inputCount, innerLayerNodeCount, outputLayerNodeCount):
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

    outfile = open("Sem2W_2.txt","w")
    outfile.write(str(weight))
    outfile.close()

netDimentions = [12,5,2]
makeRandomNN1(netDimentions[0],netDimentions[1],netDimentions[2])
makeRandomNN2(netDimentions[0],netDimentions[1],netDimentions[2])
 





