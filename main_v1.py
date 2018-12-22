import math
import random
import numpy
import pandas
import matplotlib

class Individual:
    def __init__(self,aNumber):
        self.number = aNumber
    def getNumber(self):
        return(self.number)

class Population:
    def __init__(self):
        self.members = []
        self.max = 0
    def addIndividual(self,aIndividual):
        self.members.append(aIndividual)
        aMax = self.getMax()
        aNumber = aIndividual.getNumber()
        if aMax < aNumber:
            aMax = aNumber
            self.setMax(aNumber)
    def getIndividuals(self):
        return self.members
    def getNumbers(self):
        lNumber = []
        for people in self.members:
            lNumber.append(people.getNumber())
        return lNumber
    def getPopSize(self):
        return len(self.members)
    def setMax(self,aMax):
        self.max = aMax
    def getMax(self):
        return self.max


def reproduce(aIndividual):
    return Individual(aIndividual.getNumber())

def createOffspring(aParent,aMu,aPopulation):
    if aMu > random.random():
        aMax = aPopulation.getMax()
        aNumber = aMax + 1
    else:
        aNumber = aParent.getNumber()
    return Individual(aNumber)

def getUnique(lTemp):
    return list(set(lTemp))

def createIndividual(aNumber,lAllPastAndPresentIndividuals):
    lAllPastAndPresentIndividuals.append(aNumber)
    return Individual(aNumber)

def createInitialPopulation(aPopSize,aMax):
    aPopulation = Population()
    for i in range(0,aPopSize):
        aIndividual = Individual(random.randint(1,aMax))
        aPopulation.addIndividual(aIndividual)
    aPopulation.setMax(max(aPopulation.getNumbers()))
    return aPopulation

def populationReproduce(aPopulation,aMu):
    bPopulation = Population()
    bPopulation.setMax(aPopulation.getMax())
    lParents = aPopulation.getIndividuals()
    aPopSize = aPopulation.getPopSize()
    for i in range(0,aPopSize):
        aRand = random.randint(0,aPopSize-1)
        aIndividual = createOffspring(lParents[aRand],aMu,bPopulation)
        bPopulation.addIndividual(aIndividual)
    return bPopulation


def runAll(aNumGenerations,aPopSize,aMu,aMax):
    lPops = []
    aInitialPopulation = createInitialPopulation(aPopSize,aMax)
    lPops.append(aInitialPopulation)
    lExisting = list(set(aInitialPopulation.getNumbers()))
    for generations in range(1,aNumGenerations):
        # print(generations)
        aParents = lPops[generations-1]
        lExisting = lExisting + aParents.getNumbers()
        lExisting = list(set(lExisting))
        aChildren = populationReproduce(aParents,aMu)
        lPops.append(aChildren)
    return lPops

def getArray(lPops):
    lNumbers = []
    for pops in lPops:
        lNumbers.append(pops.getNumbers())
    lNumbers = numpy.array(lNumbers)
    return lNumbers

def getFlatList(lPops):
    aArray = getArray(lPops)
    return aArray.flatten()

def getCounts(lPops):
    lNumbers = getFlatList(lPops)
    lNumbers = pandas.Series(lNumbers)
    return lNumbers.value_counts()


vMu = [0.004,0.008,0.016,0.032,0.064,0.128]

for i in range(0,len(vMu)):
    for j in range(0,5):
        print("i = " + str(i) + ", j = " + str(j))
        lTest = runAll(1000,250,vMu[i],250)
        lTemp = getCounts(lTest)
        aName = "test_" + str(i) + "_" + str(j) + ".csv"
        lTemp.to_csv(aName, sep=',')

print lTemp
print len(lTemp)
