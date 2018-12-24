import Bentley
import numpy as np
import copy


# Wright-Fisher/Bentley
# For each offspring parent is chosen in proportion to its frequency if
# aBeta != 0
def populationReproduceFrequency(aPopulation, aMu0, aBeta):
    bPopulation = Bentley.Population()
    bPopulation.setMax(aPopulation.getMax())
    aPopSize = aPopulation.getPopSize()
    lParents = aPopulation.getIndividuals()
    parent_weight = calculate_weight(aPopulation, lParents, aPopSize, aBeta)
    for i in range(0, aPopSize):
        aRand = np.random.choice(aPopSize, size=1, p=parent_weight)[0]
        aIndividual = Bentley.createOffspring(lParents[aRand], aMu0,
                                              bPopulation)
        bPopulation.addIndividual(aIndividual)
    bPopulation.calculateAllFreq()
    return bPopulation


# For Moran where you just pick one parent and reproduce (this can be weighted)
# and you kill any parent at random
def populationReproduceMoran(aPopulation, aMu0, aBeta):
    bPopulation = copy.deepcopy(aPopulation)
    aPopSize = bPopulation.getPopSize()

    # pick one parent to reproduce (using weights) and one to kill per cycle
    for i in range(0, aPopSize):
        lParents = bPopulation.getIndividuals()
        parent_weight = calculate_weight(bPopulation, lParents,
                                         aPopSize, aBeta)
        # pick individual to reproduce
        aRand = np.random.choice(aPopSize, size=1, p=parent_weight)[0]
        aIndividual = Bentley.createOffspring(lParents[aRand], aMu0,
                                              bPopulation)
        bPopulation.addIndividual(aIndividual)

        # pick individual to kill
        bRand = np.random.randint(aPopSize)
        bPopulation.killIndividual(lParents[bRand])
        assert bPopulation.getPopSize() == aPopSize
        bPopulation.calculateAllFreq()
    return bPopulation


# Same as Moran but no one dies (i.e. population grows)
def populationReproduceYule(aPopulation, aMu0, aBeta):
    bPopulation = copy.deepcopy(aPopulation)
    aPopSize = bPopulation.getPopSize()

    for i in range(0, aPopSize):
        lParents = bPopulation.getIndividuals()
        aPopSize = bPopulation.getPopSize()
        parent_weight = calculate_weight(bPopulation, lParents,
                                         aPopSize, aBeta)
        # pick individual to reproduce
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


def runAllMoranFrequency(aNumGenerations, aPopSize, aMu0, aBeta, aMax):
    lPops = []
    aInitialPopulation = Bentley.createInitialPopulation(aPopSize, aMax)
    lPops.append(aInitialPopulation)
    lExisting = list(set(aInitialPopulation.getNumbers()))
    for generations in range(1, aNumGenerations):
        # print(generations)
        aParents = lPops[generations-1]
        lExisting = lExisting + aParents.getNumbers()
        lExisting = list(set(lExisting))
        aChildren = populationReproduceMoran(aParents, aMu0, aBeta)
        lPops.append(aChildren)
    return lPops


def runAllYuleFrequency(aNumGenerations, aPopSize, aMu0, aBeta, aMax):
    lPops = []
    aInitialPopulation = Bentley.createInitialPopulation(aPopSize, aMax)
    lPops.append(aInitialPopulation)
    lExisting = list(set(aInitialPopulation.getNumbers()))
    for generations in range(1, aNumGenerations):
        # print(generations)
        aParents = lPops[generations-1]
        lExisting = lExisting + aParents.getNumbers()
        lExisting = list(set(lExisting))
        aChildren = populationReproduceYule(aParents, aMu0, aBeta)
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


def calculate_weight(aPopulation, lParents, aPopSize, aBeta):
    cnt = aPopulation.getAllFreq()
    parent_weight = np.zeros(aPopSize)
    # cnt[parent] / aPopSize is the frequency of the parental variant
    for i, parent in enumerate(lParents):
        parent_weight[i] = (1 + (float(cnt[parent.getNumber()]) / aPopSize)
                            * aBeta)
    # normalise parent weight
    parent_weight = parent_weight / np.sum(parent_weight)
    return parent_weight
