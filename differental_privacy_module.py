"""
This module contains the implementation of guessing advantage to add the differential privacy.
The module should be able to retun the DFG after adding the noise.
The module has two main functionalities:
    * Take delta as input, then calculate both epsilon and accuracy correlated with it.
    * Take accuracy as input, then calculate both epsilon and the delta (risk) correlated with it.
"""
from guessing_advantage import calculate_epsilon_freq , calculate_epsilon_from_delta, calculate_epsilon_time, AggregateType
import diffprivlib.mechanisms as privacyMechanisms
from convert_dfg import calculate_time_dfg
import sys
from measure_accuracy import earth_mover_dist
from collections import Counter

def differential_privacy_with_risk( dfg_freq, dfg_time, delta, precision, aggregate_type=AggregateType.SUM):
    """
    This method adds the differential privacy to the DFG of both time and frequencies.
        * It calculates the epsilon using the guessing advantage technique.
        * It adds laplace noise to the DFGs.
        * It calculates the distance resulted from the noise
    """
    accuracy=1
    # calculate epsilon
    epsilon_freq,senstivity_freq=calculate_epsilon_freq(dfg_freq,delta)
    epsilon_time,senstivity_time=calculate_epsilon_time(dfg_time,delta,precision, aggregate_type)




    # adding laplace noise to DFG frequencies
    laplace_mechanism = privacyMechanisms.LaplaceBoundedDomain()
    laplace_mechanism.set_sensitivity(senstivity_freq).set_bounds(0, sys.maxsize).set_epsilon(epsilon_freq)


    dfg_freq_new = Counter()
    for key in dfg_freq.keys():
        dfg_freq_new[key]= laplace_mechanism.randomise(dfg_freq[key])

    # adding laplace noise to DFG time

    # calculate the DFG for the time
    dfg_time= calculate_time_dfg(dfg_time,aggregate_type)
    dfg_time_new = Counter()
    for key in dfg_time.keys():
        laplace_mechanism.set_sensitivity(senstivity_time).set_bounds(0, sys.maxsize).set_epsilon(epsilon_time[key])
        dfg_time_new[key]= laplace_mechanism.randomise(dfg_time[key])


    # Calculate earth moving distance
    emd_freq=earth_mover_dist(dfg_freq,dfg_freq_new)
    emd_time=earth_mover_dist(dfg_time,dfg_time_new)
    return dfg_freq_new, dfg_time_new, epsilon_freq,epsilon_time, emd_freq, emd_time




def differential_privacy_with_accuracy( dfg_freq, dfg_time, accuracy):
    epsilon=1
    delta=1

    # TODO calculate epsilon

    # TODO adding laplace noise

    # TODO Calculate delta ( the risk)
    return dfg_freq, dfg_time, epsilon, delta