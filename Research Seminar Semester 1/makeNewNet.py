
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

makeRandomNN(21,8,3)