"""
In this module, we implement the accuracy measures to evaluate the effect of differential privacy injection.
In this module, we support the following measures:
    * F1-score.
    * Earth Mover's distance.
"""

from scipy.stats import wasserstein_distance
from math import fabs
def earth_mover_dist(dfg1, dfg2):
    #  need to consider for zero frequncies as the counter object don't include it
    # after the discussion, we decided to let the user know about that issue and maybe has can handle it on his own.
    v1=list(dfg1.values())
    v2=list(dfg2.values())

    distance = wasserstein_distance(v1,v2)

    return distance

def percentage_dist(dfg1,dfg2):
    #returns the maximum percentage difference between the two DFGs
    distance =0
    for key in dfg1.keys():
        diff = fabs(dfg1[key]-dfg2[key])/dfg1[key]
        if diff>distance:
            distance=diff
    return distance