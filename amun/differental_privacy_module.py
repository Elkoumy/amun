"""
This module contains the implementation of guessing advantage to add the differential privacy.
The module should be able to retun the DFG after adding the noise.
The module has two main functionalities:
    * Take delta as input, then calculate both epsilon and accuracy correlated with it.
    * Take accuracy as input, then calculate both epsilon and the delta (risk) correlated with it.
"""
from amun.guessing_advantage import calculate_epsilon_freq, calculate_epsilon_time, \
    AggregateType, calculate_epsilon_from_distance_time_percentage_distance, calculate_epsilon_from_distance_freq_percentage_distances
import diffprivlib.mechanisms as privacyMechanisms
from amun.convert_dfg import calculate_time_dfg
import sys
from amun.measure_accuracy import earth_mover_dist, percentage_dist
from collections import Counter
from scipy.stats import laplace
from math import inf
# from diffprivlib.mechanisms import Laplace

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

    #calculating the percentage difference
    percent_freq, percent_freq_dist=percentage_dist(dfg_freq,dfg_freq_new)
    percent_time, percent_time_dist=percentage_dist(dfg_time,dfg_time_new)


    return dfg_freq_new, dfg_time_new, epsilon_freq,epsilon_time, emd_freq, emd_time, percent_freq,percent_time,percent_freq_dist,percent_time_dist


def add_laplace_noise_time(aggregate_type, dfg_time, epsilon_time):
    laplace_mechanism = privacyMechanisms.LaplaceBoundedDomain()


    sens_time = 1
    """ calculating sensitivity based on type of aggregate"""
    if aggregate_type == AggregateType.AVG:
        # sens_time = 1.0 / len(dfg_time[0])
        sens_time = 1.0 / len(dfg_time.keys())

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

            # in case epsilon is inf , we don't need to add noise
            # print("epsilon_time"+str(epsilon_time[key]))
            # inf in case of risk is bigger than 1-p_k
            # -inf in case of all the values are the same.
            # small epsilon values fail with laplace function
            if epsilon_time[key]==inf or epsilon_time[key]==-inf or epsilon_time[key]<1e-11:
                dfg_time_new[key] = dfg_time[key]
            else:
                laplace_mechanism.set_sensitivity(sens_time).set_bounds(0, sys.maxsize).set_epsilon(epsilon_time[key])
                dfg_time_new[key] = laplace_mechanism.randomise(dfg_time[key])

            # laplace = Laplace()
            # laplace.set_epsilon(epsilon_time[key])
            # laplace.set_sensitivity(sens_time)
            # dfg_time_new[key]=laplace.randomise(dfg_time[key])
    else:
        # single epsilon value for the entire time dfg
        for key in dfg_time.keys():

            # in case epsilon is inf , we don't need to add noise
            if epsilon_time == inf:
                dfg_time_new[key] = dfg_time[key]
            else:
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
    # laplace_mechanism = privacyMechanisms.LaplaceBoundedDomain()
    # laplace_mechanism.set_sensitivity(senstivity_freq).set_bounds(0, sys.maxsize).set_epsilon(epsilon_freq)
    dfg_freq_new = Counter()
    for key in dfg_freq.keys():
        # dfg_freq_new[key] = laplace_mechanism.randomise(dfg_freq[key])

        # laplace = Laplace()
        # laplace.set_epsilon(epsilon_freq)
        # laplace.set_sensitivity(senstivity_freq)
        # dfg_freq_new[key] = laplace.randomise(dfg_freq[key])
        rv = laplace()

        if type(epsilon_freq)==type(0.1):
            #single epsilon value
            dfg_freq_new[key] = dfg_freq[key]+laplace.rvs(loc=0,scale=senstivity_freq/epsilon_freq,size=1)[0]
        else:
            #multiple epsilon value
            dfg_freq_new[key] = dfg_freq[key] + laplace.rvs(loc=0, scale=senstivity_freq / epsilon_freq[key], size=1)[0]

    return dfg_freq_new


def differential_privacy_with_accuracy( dfg_freq, dfg_time,precision, distance,aggregate_type=AggregateType.SUM):
    #calculate epsilon and delta for  freq
    # epsilon_freq, delta_freq=calculate_epsilon_from_distance_freq(dfg_freq,  distance)
    epsilon_freq, delta_freq_dfg , delta_freq = calculate_epsilon_from_distance_freq_percentage_distances(dfg_freq, distance)

    # calculate epsilon and delta for  time
    # epsilon_time,  delta_time, delta_time_dfg = calculate_epsilon_from_distance_time( dfg_time, distance,precision, aggregate_type)
    # epsilon_time, delta_time, delta_time_dfg = calculate_epsilon_from_distance_time_new_approach(dfg_time, distance, precision, aggregate_type)
    epsilon_time, delta_time, delta_time_dfg = calculate_epsilon_from_distance_time_percentage_distance(dfg_time, distance, precision,aggregate_type)
    #  apply laplace noise and return the noisfied version of the DFG.

    # adding laplace noise to DFG freq
    dfg_freq_new = add_laplace_noise_freq(dfg_freq, epsilon_freq)

    # adding laplace noise to DFG time
    dfg_time, dfg_time_new = add_laplace_noise_time(aggregate_type, dfg_time, epsilon_time)

    return dfg_freq_new, dfg_time_new, epsilon_freq, epsilon_time, delta_freq , delta_time , delta_freq_dfg, delta_time_dfg


def risk_pruning(dfg_freq, dfg_time, dfg_delta_freq, dfg_delta_time, risk_pruning):
    keys = list(dfg_freq.keys())
    for key in keys:
        if dfg_delta_freq[key]<risk_pruning or dfg_delta_time[key]<risk_pruning:
            del dfg_freq[key]
            del dfg_time[key]
            del dfg_delta_freq[key]
            del dfg_delta_time[key]

    return dfg_freq, dfg_time, dfg_delta_freq, dfg_delta_time