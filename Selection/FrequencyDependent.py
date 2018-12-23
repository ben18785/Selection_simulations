from Selection import Bentley
import random
import numpy
import pandas
from scipy.stats import logistic

# Prob of producing identical offspring for object i = alpha + beta * # copies of i
def createOffspringFrequency(aParent,aMu0,aBeta,aPopulation,bPopulation):
    aFreq = float(aPopulation.getVariantFreq(aParent.getNumber())) / float(aPopulation.getPopSize())
    aProb = logistic.cdf(logistic.ppf(1-aMu0) + aBeta * aFreq)
    if aProb > random.random():
        aNumber = aParent.getNumber()
    else:
        aMax = bPopulation.getMax()
        aNumber = aMax + 1
    return Bentley.Individual(aNumber)

def populationReproduceFrequency(aPopulation,aMu0,aBeta):
    bPopulation = Bentley.Population()
    bPopulation.setMax(aPopulation.getMax())
    lParents = aPopulation.getIndividuals()
    aPopSize = aPopulation.getPopSize()
    for i in range(0,aPopSize):
        aRand = random.randint(0,aPopSize-1)
        aIndividual = createOffspringFrequency(lParents[aRand],aMu0,aBeta,aPopulation,bPopulation)
        bPopulation.addIndividual(aIndividual)
    return bPopulation


def runAllFrequency(aNumGenerations,aPopSize,aMu0,aBeta,aMax):
    lPops = []
    aInitialPopulation = Bentley.createInitialPopulation(aPopSize,aMax)
    lPops.append(aInitialPopulation)
    lExisting = list(set(aInitialPopulation.getNumbers()))
    for generations in range(1,aNumGenerations):
        # print(generations)
        aParents = lPops[generations-1]
        lExisting = lExisting + aParents.getNumbers()
        lExisting = list(set(lExisting))
        aChildren = populationReproduceFrequency(aParents,aMu0,aBeta)
        lPops.append(aChildren)
    return lPops

def replicates(i,bName,aNumIter,aNumGenerations,aPopSize,aMu0,aBeta,aMax):
    for j in range(0,aNumIter):
        print("i = " + str(i) + ", j = " + str(j))
        lTest = runAllFrequency(aNumGenerations,aPopSize,aMu0,aBeta,aMax)
        lTemp = Bentley.getCounts(lTest)
        aName = bName + str(i) + "_" + str(j) + ".csv"
        lTemp.to_csv(aName, sep=',')

def createOffspringFrequencyMean(aParent, aMu0, aBeta, aPopulation, bPopulation):
    aFreq = float(aPopulation.getVariantFreq(aParent.getNumber())) / float(aPopulation.getPopSize())
    aProb = logistic.cdf(logistic.ppf(1 - aMu0) + aBeta * (aFreq - aPopulation.getMeanVariantFreq()))
    if aProb > random.random():
        aNumber = aParent.getNumber()
    else:
        aMax = bPopulation.getMax()
        aNumber = aMax + 1
    return Bentley.Individual(aNumber)


def populationReproduceFrequencyMean(aPopulation,aMu0,aBeta):
    bPopulation = Bentley.Population()
    bPopulation.setMax(aPopulation.getMax())
    lParents = aPopulation.getIndividuals()
    aPopSize = aPopulation.getPopSize()
    for i in range(0,aPopSize):
        aRand = random.randint(0,aPopSize-1)
        aIndividual = createOffspringFrequencyMean(lParents[aRand],aMu0,aBeta,aPopulation,bPopulation)
        bPopulation.addIndividual(aIndividual)
    return bPopulation


def runAllFrequencyMean(aNumGenerations,aPopSize,aMu0,aBeta,aMax):
    lPops = []
    aInitialPopulation = Bentley.createInitialPopulation(aPopSize,aMax)
    lPops.append(aInitialPopulation)
    lExisting = list(set(aInitialPopulation.getNumbers()))
    for generations in range(1,aNumGenerations):
        # print(generations)
        aParents = lPops[generations-1]
        lExisting = lExisting + aParents.getNumbers()
        lExisting = list(set(lExisting))
        aChildren = populationReproduceFrequencyMean(aParents,aMu0,aBeta)
        lPops.append(aChildren)
    return lPops

def replicatesMean(i,bName,aNumIter,aNumGenerations,aPopSize,aMu0,aBeta,aMax):
    for j in range(0,aNumIter):
        print("i = " + str(i) + ", j = " + str(j))
        lTest = runAllFrequencyMean(aNumGenerations,aPopSize,aMu0,aBeta,aMax)
        lTemp = Bentley.getCounts(lTest)
        aName = bName + str(i) + "_" + str(j) + ".csv"
        lTemp.to_csv(aName, sep=',')
