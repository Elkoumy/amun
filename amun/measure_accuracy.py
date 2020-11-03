"""
In this module, we implement the accuracy measures to evaluate the effect of differential privacy injection.
In this module, we support the following measures:
    * F1-score.
    * Earth Mover's distance.
"""

from scipy.stats import wasserstein_distance
from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.evaluation.replay_fitness import factory as replay_factory
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
    distance_dist={}
    for key in dfg1.keys():
        if dfg1[key]!=0: #division by zero
            diff = fabs(dfg1[key]-dfg2[key])/dfg1[key]
        else:
            diff = fabs( ((100-dfg1[key]) - (100-dfg2[key])) / (100-dfg1[key]) )
        distance_dist[key]=diff
        if diff>distance:
            distance=diff
    return distance, distance_dist


def error_calculation(dfg1,dfg2):
    #return MAPE, SMAPE, and distribution of APE between two DFGs.
    total =0
    smape_acc=0
    APE_dist={}
    MAPE_dist={}
    SMAPE_dist={}
    """************parallel by edge******************"""
    for key in dfg1.keys():
        if dfg1[key]!=0: #division by zero
            diff = fabs(dfg1[key]-dfg2[key])/fabs(dfg1[key])
            smape= abs(dfg1[key] - dfg2[key]) / abs(dfg1[key] + dfg2[key])
        else:
            diff = fabs( ((100-dfg1[key]) - (100-dfg2[key])) / fabs(100-dfg1[key]) )
            smape= abs((100-dfg1[key] )- (100-dfg2[key])) / abs((100-dfg1[key]) + (100-dfg2[key]))

        APE_dist[key]=diff
        smape_acc +=smape
        SMAPE_dist[key]=smape


        # smape_acc+=abs(dfg1[key]-dfg2[key])/(dfg1[key]+dfg2[key])
        total+=diff

    MAPE= total/len(dfg1.keys())

    SMAPE=smape_acc/len(dfg1.keys())

    return MAPE, SMAPE, APE_dist, SMAPE_dist

def f1_score(xes_file,dfg1,dfg2):
    f1_score_1, f1_score_2=0,0
    #first we use inductive miner to generate the petric nets of both the DFGs
    net1, initial_marking1, final_marking1 = inductive_miner.apply(dfg1)
    net2, initial_marking2, final_marking2 = inductive_miner.apply(dfg2)
    fitness_1 = replay_factory.apply(xes_file, net1, initial_marking1, final_marking1)
    fitness_2 = replay_factory.apply(xes_file, net2, initial_marking2, final_marking2)

    return fitness_1, fitness_2