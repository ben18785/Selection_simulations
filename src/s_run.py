import sys
from Selection import Models
import pandas
import time
start = time.time()

selection = float(sys.argv[1])
aNumGenerations = 5000000
aPopSize = 1000
aMu0 = 0.001
aInitialPopulation, changes = Models.MoranRun(aNumGenerations, aPopSize, aMu0, selection, aPopSize)
pandas.DataFrame.from_dict(aInitialPopulation, orient='index').reset_index().to_csv("../data/negative_yule_moran/moran_initial_" + str(selection) + ".csv", sep=',')
pandas.DataFrame(changes).to_csv("../data/negative_yule_moran/moran_changes_" + str(selection) + ".csv", sep=',')
end = time.time()
print(str(aNumGenerations) + " generations took " + str(end - start))
