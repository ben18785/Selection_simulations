import sys
from Selection import Models
import pandas

selection = float(sys.argv[1])
aNumGenerations = 5
aPopSize = 1000
aMu0 = 0.001
aDF = Models.MoranRun(aNumGenerations, aPopSize, aMu0, selection, aPopSize)
pandas.DataFrame(aDF).to_csv("../data/negative_yule_moran/moran_" + str(selection) + ".csv", sep=',')
