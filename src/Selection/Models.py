import Bentley
import FrequencyDependent
import pandas


def WrightFisherRun(aNumGenerations, aPopSize, aMu0, aBeta, aMax):
    lPops = FrequencyDependent.runAllFrequency(aNumGenerations, aPopSize, aMu0,
                                               aBeta, aMax)
    aDF = Bentley.time_series(lPops)
    aDF = pandas.DataFrame(aDF)
    aDF.columns = ["generation", "variant", "count"]
    return aDF


def MoranRun(aNumGenerations, aPopSize, aMu0, aBeta, aMax):
    aInitialPopulation, add, kill = FrequencyDependent.runAllMoranFrequency(
        aNumGenerations, aPopSize, aMu0, aBeta, aMax)
    aDF = pandas.DataFrame({'added': add,
                            'killed': kill})
    return aInitialPopulation.getAllFreq(), aDF


def YuleRun(aNumGenerations, aPopSize, aMu0, aBeta, aMax):
    aInitialPopulation, add = FrequencyDependent.runAllYuleFrequency(
        aNumGenerations, aPopSize, aMu0, aBeta, aMax)
    aDF = pandas.DataFrame({'added': add})
    return aInitialPopulation.getAllFreq(), aDF
