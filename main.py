import math
import random
import numpy
import pandas

class Individual:
    def __init__(self,aNumber):
        self.number = aNumber
    def getNumber(self):
        return(self.number)

class Population:
    def __init__(self):
        self.members = []
    def addIndividual(self,aIndividual):
        self.members.append(aIndividual)
    def getIndividuals(self):
        return self.members
    def getNumbers(self):
        lNumber = []
        for people in self.members:
            lNumber.append(people.getNumber())
        return lNumber
    def getPopSize(self):
        return len(self.members)


def reproduce(aIndividual):
    return Individual(aIndividual.getNumber())

def createOffspring(aParent,aMu,lExisting,aMax):
    if aMu > random.random():
        aNumber = random.randint(1,aMax)
        while aNumber in lExisting:
            aNumber = random.randint(1, aMax)
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
    return aPopulation

def populationReproduce(aPopulation,aMu,lExisting,aMax):
    bPopulation = Population()
    lParents = aPopulation.getIndividuals()
    aPopSize = aPopulation.getPopSize()
    for i in range(0,aPopSize):
        aRand = random.randint(0,aPopSize-1)
        aIndividual = createOffspring(lParents[aRand],aMu,lExisting,aMax)
        bPopulation.addIndividual(aIndividual)
    return bPopulation


def runAll(aNumGenerations,aPopSize,aMu,aMax):
    lPops = []
    aInitialPopulation = createInitialPopulation(aPopSize,aMax)
    lPops.append(aInitialPopulation)
    lExisting = list(set(aInitialPopulation.getNumbers()))
    for generations in range(1,aNumGenerations):
        aParents = lPops[generations-1]
        lExisting = lExisting + aParents.getNumbers()
        lExisting = list(set(lExisting))
        aChildren = populationReproduce(aParents,aMu,lExisting,aMax)
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


lTest = runAll(1000,250,0.001,1000000)

lTemp = getCounts(lTest)

print lTemp
print len(lTemp)