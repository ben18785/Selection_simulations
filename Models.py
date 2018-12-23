from Selection import Bentley
from Selection import FrequencyDependent
import pandas


def WrightFisherRun(aNumGenerations, aPopSize, aMu0, aBeta, aMax):
    lPops = FrequencyDependent.runAllFrequency(aNumGenerations, aPopSize, aMu0,
                                               aBeta, aMax)
    aDF = Bentley.time_series(lPops)
    aDF = pandas.DataFrame(aDF)
    aDF.columns = ["generation", "variant", "count"]
    return aDF
