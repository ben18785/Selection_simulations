from Selection import Bentley
import numpy as np


# for each offspring parent is chosen in proportion to its frequency if
# aBeta != 0
def populationReproduceFrequency(aPopulation, aMu0, aBeta):
    bPopulation = Bentley.Population()
    bPopulation.setMax(aPopulation.getMax())
    lParents = aPopulation.getIndividuals()
    aPopSize = aPopulation.getPopSize()
    cnt = aPopulation.getAllFreq()
    parent_weight = np.zeros(aPopSize)
    # cnt[parent] / aPopSize is the frequency of the parental variant
    for i, parent in enumerate(lParents):
        parent_weight[i] = 1 + (float(cnt[parent]) / aPopSize) * aBeta
    # normalise parent weight
    parent_weight = parent_weight / np.sum(parent_weight)
    for i in range(0, aPopSize):
        aRand = np.random.choice(aPopSize, size=1, p=parent_weight)[0]
        aIndividual = Bentley.createOffspring(lParents[aRand], aMu0,
                                              bPopulation)
        bPopulation.addIndividual(aIndividual)
    bPopulation.calculateAllFreq()
    return bPopulation


def runAllFrequency(aNumGenerations, aPopSize, aMu0, aBeta, aMax):
    lPops = []
    aInitialPopulation = Bentley.createInitialPopulation(aPopSize, aMax)
    lPops.append(aInitialPopulation)
    lExisting = list(set(aInitialPopulation.getNumbers()))
    for generations in range(1, aNumGenerations):
        # print(generations)
        aParents = lPops[generations-1]
        lExisting = lExisting + aParents.getNumbers()
        lExisting = list(set(lExisting))
        aChildren = populationReproduceFrequency(aParents, aMu0, aBeta)
        lPops.append(aChildren)
    return lPops


def replicates(i, bName, aNumIter, aNumGenerations, aPopSize, aMu0, aBeta,
               aMax):
    for j in range(0, aNumIter):
        print("i = " + str(i) + ", j = " + str(j))
        lTest = runAllFrequency(aNumGenerations, aPopSize, aMu0, aBeta, aMax)
        lTemp = Bentley.getCounts(lTest)
        aName = bName + str(i) + "_" + str(j) + ".csv"
        lTemp.to_csv(aName, sep=',')
