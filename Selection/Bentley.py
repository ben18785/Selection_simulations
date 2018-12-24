import random
import numpy
import pandas
import collections


class Individual:
    def __init__(self, aNumber):
        self.number = aNumber

    def getNumber(self):
        return(self.number)


class Population:
    def __init__(self):
        self.members = []
        self.max = 0
        self.cnt = collections.Counter()

    def addIndividual(self, aIndividual):
        self.members.append(aIndividual)
        aMax = self.getMax()
        aNumber = aIndividual.getNumber()
        if aMax < aNumber:
            self.setMax(aNumber)

    def killIndividual(self, aIndividual):
        self.members.remove(aIndividual)

    def getIndividuals(self):
        return self.members

    def getNumbers(self):
        lNumber = []
        for people in self.members:
            lNumber.append(people.getNumber())
        return lNumber

    def getPopSize(self):
        return len(self.members)

    def setMax(self, aMax):
        self.max = aMax

    def getMax(self):
        return self.max

    def getNumberCount(self):
        lNumbers = pandas.Series(self.getNumbers())
        return lNumbers.value_counts()

    def getVariantFreq(self, aNumber):
        lTemp = self.getNumberCount()
        lTemp = lTemp.to_frame()
        lTemp['number'] = lTemp.index
        lBool = lTemp['number'].isin([aNumber])
        aInd = lBool.to_frame().iloc[:, 0].sum()
        if aInd > 0:
            aValue = lTemp[lBool]
            aFreq = aValue.iloc[0, 0]
        else:
            aFreq = 0
        return aFreq

    def getMeanVariantFreq(self):
        return (self.getNumberCount() / self.getPopSize()).mean()

    def calculateAllFreq(self):
        self.cnt = collections.Counter()
        for people in self.members:
            a_number = people.getNumber()
            self.cnt[a_number] += 1

    def getAllFreq(self):
        return self.cnt


def createOffspring(aParent, aMu, aPopulation):
    if aMu > random.random():
        aMax = aPopulation.getMax()
        aNumber = aMax + 1
    else:
        aNumber = aParent.getNumber()
    return Individual(aNumber)


def getUnique(lTemp):
    return list(set(lTemp))


def createIndividual(aNumber, lAllPastAndPresentIndividuals):
    lAllPastAndPresentIndividuals.append(aNumber)
    return Individual(aNumber)


def createInitialPopulation(aPopSize, aMax):
    aPopulation = Population()
    for i in range(0, aPopSize):
        aIndividual = Individual(random.randint(1, aMax))
        aPopulation.addIndividual(aIndividual)
    aPopulation.setMax(max(aPopulation.getNumbers()))
    aPopulation.calculateAllFreq()
    return aPopulation


def populationReproduce(aPopulation, aMu):
    bPopulation = Population()
    bPopulation.setMax(aPopulation.getMax())
    lParents = aPopulation.getIndividuals()
    aPopSize = aPopulation.getPopSize()
    for i in range(0, aPopSize):
        aRand = random.randint(0, aPopSize-1)
        aIndividual = createOffspring(lParents[aRand], aMu, bPopulation)
        bPopulation.addIndividual(aIndividual)
    bPopulation.calculateAllFreq()
    return bPopulation


def runAll(aNumGenerations, aPopSize, aMu, aMax):
    lPops = []
    aInitialPopulation = createInitialPopulation(aPopSize, aMax)
    lPops.append(aInitialPopulation)
    lExisting = list(set(aInitialPopulation.getNumbers()))
    for generations in range(1, aNumGenerations):
        # print(generations)
        aParents = lPops[generations-1]
        lExisting = lExisting + aParents.getNumbers()
        lExisting = list(set(lExisting))
        aChildren = populationReproduce(aParents, aMu)
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
    lFlat = []
    for i, pop in enumerate(lPops):
        lFlat += aArray[i]
    return lFlat


def getCounts(lPops):
    lNumbers = getFlatList(lPops)
    lNumbers = pandas.Series(lNumbers)
    return lNumbers.value_counts()


def getCounters(lPops):
    lCounters = []
    for pop in lPops:
        lCounters.append(pop.getAllFreq())
    return lCounters


def time_series(lPops):
    lCounters = getCounters(lPops)
    lkeys = list(set(getFlatList(lPops)))
    aNumGenerations = len(lCounters)
    aNumKeys = len(lkeys)
    k = 0
    aDF = numpy.zeros((aNumGenerations * aNumKeys, 3))
    for i in range(aNumGenerations):
        for j, key in enumerate(lkeys):
            aDF[k, :] = numpy.array([i + 1, key, lCounters[i][key]])
            k += 1
    aDF = aDF[aDF[:, 2] != 0, :]
    return aDF
