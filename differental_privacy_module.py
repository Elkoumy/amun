"""
This module contains the implementation of guessing advantage to add the differential privacy.
The module should be able to retun the DFG after adding the noise.
The module has two main functionalities:
    * Take delta as input, then calculate both epsilon and accuracy correlated with it.
    * Take accuracy as input, then calculate both epsilon and the delta (risk) correlated with it.
"""
from guessing_advantage import calculate_epsilon_freq , calculate_epsilon_from_distance_freq, calculate_epsilon_from_distance_time, calculate_epsilon_time, AggregateType
import diffprivlib.mechanisms as privacyMechanisms
from convert_dfg import calculate_time_dfg
import sys
from measure_accuracy import earth_mover_dist
from collections import Counter
from scipy.stats import laplace
# from diffprivlib.mechanisms import Laplace

from math import log,exp ,sqrt

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

    # adding laplace noise to DFG freq
    dfg_freq_new = add_laplace_noise_freq(dfg_freq, epsilon_freq)

    # adding laplace noise to DFG time
    dfg_time, dfg_time_new = add_laplace_noise_time(aggregate_type, dfg_time, epsilon_time)

    # Calculate earth moving distance
    emd_freq=earth_mover_dist(dfg_freq,dfg_freq_new)
    emd_time=earth_mover_dist(dfg_time,dfg_time_new)

    return dfg_freq_new, dfg_time_new, epsilon_freq,epsilon_time, emd_freq, emd_time


def add_laplace_noise_time(aggregate_type, dfg_time, epsilon_time):
    laplace_mechanism = privacyMechanisms.LaplaceBoundedDomain()


    sens_time = 1
    """ calculating sensitivity based on type of aggregate"""
    if aggregate_type == AggregateType.AVG:
        sens_time = 1 / len(dfg_time[0])
    elif aggregate_type == AggregateType.MAX or aggregate_type == AggregateType.MIN or aggregate_type == AggregateType.SUM:
        sens_time = 1
    else:
        assert "Wrong aggregate type"
    # calculate the DFG for the time
    dfg_time = calculate_time_dfg(dfg_time, aggregate_type)
    dfg_time_new = Counter()

    if type(epsilon_time) != type(0.1):
        # multiple epsilon values for the time dfg
        for key in dfg_time.keys():
            laplace_mechanism.set_sensitivity(sens_time).set_bounds(0, sys.maxsize).set_epsilon(epsilon_time[key])
            dfg_time_new[key] = laplace_mechanism.randomise(dfg_time[key])

            # laplace = Laplace()
            # laplace.set_epsilon(epsilon_time[key])
            # laplace.set_sensitivity(sens_time)
            # dfg_time_new[key]=laplace.randomise(dfg_time[key])
    else:
        # single epsilon value for the entire time dfg
        for key in dfg_time.keys():
            laplace_mechanism.set_sensitivity(sens_time).set_bounds(0, sys.maxsize).set_epsilon(epsilon_time)
            dfg_time_new[key] = laplace_mechanism.randomise(dfg_time[key])

            # laplace = Laplace()
            # laplace.set_epsilon(epsilon_time)
            # laplace.set_sensitivity(sens_time)
            # dfg_time_new[key]=laplace.randomise(dfg_time[key])

    return dfg_time, dfg_time_new


def add_laplace_noise_freq(dfg_freq, epsilon_freq):
    senstivity_freq=1
    # adding laplace noise to DFG frequencies
    laplace_mechanism = privacyMechanisms.LaplaceBoundedDomain()
    laplace_mechanism.set_sensitivity(senstivity_freq).set_bounds(0, sys.maxsize).set_epsilon(epsilon_freq)
    dfg_freq_new = Counter()
    for key in dfg_freq.keys():
        # dfg_freq_new[key] = laplace_mechanism.randomise(dfg_freq[key])

        # laplace = Laplace()
        # laplace.set_epsilon(epsilon_freq)
        # laplace.set_sensitivity(senstivity_freq)
        # dfg_freq_new[key] = laplace.randomise(dfg_freq[key])

        rv = laplace()
        dfg_freq_new[key] = dfg_freq[key]+laplace.rvs(loc=0,scale=senstivity_freq/epsilon_freq,size=1)[0]

    return dfg_freq_new


def differential_privacy_with_accuracy( dfg_freq, dfg_time,precision, distance,aggregate_type=AggregateType.SUM):
    #calculate epsilon and delta for both freq and time
    epsilon_freq, delta_freq=calculate_epsilon_from_distance_freq(dfg_freq,  distance)
    epsilon_time,  delta_time = calculate_epsilon_from_distance_time( dfg_time, distance,precision, AggregateType.SUM)

    #  apply laplace noise and return the noisfied version of the DFG.

    # adding laplace noise to DFG freq
    dfg_freq_new = add_laplace_noise_freq(dfg_freq, epsilon_freq)

    # adding laplace noise to DFG time
    dfg_time, dfg_time_new = add_laplace_noise_time(aggregate_type, dfg_time, epsilon_time)

    return dfg_freq_new, dfg_time_new, epsilon_freq, epsilon_time, delta_freq , delta_time