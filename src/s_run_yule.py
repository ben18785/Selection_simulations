import sys
from Selection import Models
import pandas

selection = float(sys.argv[1])
aNumGenerations = 500
aPopSize = 1
aMu0 = 0.001
aDF = Models.YuleRun(aNumGenerations, aPopSize, aMu0, selection, aPopSize)
pandas.DataFrame(aDF).to_csv("../data/negative_yule_moran/yule_" + str(selection) + ".csv", sep=',')
