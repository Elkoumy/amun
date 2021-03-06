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
from amun.measure_accuracy import earth_mover_dist, percentage_dist, error_calculation
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


    #calculating the APE, MAPE, and SMAPE
    MAPE_freq, SMAPE_freq, APE_dist_freq,SMAPE_dist_freq=error_calculation(dfg_freq,dfg_freq_new)
    MAPE_time, SMAPE_time, APE_dist_time, SMAPE_dist_time = error_calculation(dfg_time,dfg_time_new)

    # return dfg_freq_new, dfg_time_new, epsilon_freq,epsilon_time, emd_freq, emd_time, percent_freq,percent_time,percent_freq_dist,percent_time_dist

    return dfg_freq_new, dfg_time_new, epsilon_freq,epsilon_time, MAPE_freq, SMAPE_freq, APE_dist_freq, MAPE_time, SMAPE_time, APE_dist_time, SMAPE_dist_freq, SMAPE_dist_time


def differential_privacy_with_risk( dfg,  delta, precision, aggregate_type=AggregateType.FREQ):
    """
    This method adds the differential privacy to the DFG
        * It takes the aggregate type as input including the frequency
        * It calculates the epsilon using the guessing advantage technique.
        * It adds laplace noise to the DFGs.
        * It calculates the distance resulted from the noise
    """
    accuracy=1
    # calculate epsilon
    if aggregate_type==AggregateType.FREQ:
        epsilon, senstivity_freq = calculate_epsilon_freq(dfg, delta)
        # adding laplace noise to DFG freq
        dfg_new = add_laplace_noise_freq(dfg, epsilon)
        # Calculate earth moving distance
        # emd_freq = earth_mover_dist(dfg, dfg_freq_new)
        # calculating the APE, MAPE, and SMAPE
        MAPE, SMAPE, APE_dist, SMAPE_dist = error_calculation(dfg, dfg_new)
    else:
        epsilon, senstivity = calculate_epsilon_time(dfg, delta, precision, aggregate_type)
        # adding laplace noise to DFG time
        dfg, dfg_new = add_laplace_noise_time(aggregate_type, dfg, epsilon)
        # emd_time = earth_mover_dist(dfg_time, dfg_time_new)
        MAPE, SMAPE, APE_dist, SMAPE_dist = error_calculation(dfg, dfg_new)





    return dfg_new, dfg_new, epsilon,  MAPE, SMAPE, APE_dist, SMAPE_dist


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


            if epsilon_time[key]==inf or epsilon_time[key]==-inf or epsilon_time[key]<1e-11:
                dfg_time_new[key] = dfg_time[key]
            else:
                rv = laplace()

                noise=laplace.rvs(loc=0, scale=sens_time / epsilon_time[key], size=1)[0]
                dfg_time_new[key]=dfg_time[key]+abs(noise)


    else:
        # single epsilon value for the entire time dfg
        for key in dfg_time.keys():

            # in case epsilon is inf , we don't need to add noise
            if epsilon_time == inf:
                dfg_time_new[key] = dfg_time[key]
            else:

                rv = laplace()
                noise = laplace.rvs(loc=0, scale=sens_time / epsilon_time, size=1)[0]
                dfg_time_new[key] = dfg_time[key] + abs(noise)



    return dfg_time, dfg_time_new


def add_laplace_noise_freq(dfg_freq, epsilon_freq):
    senstivity_freq=1

    dfg_freq_new = Counter()
    for key in dfg_freq.keys():

        rv = laplace()

        if type(epsilon_freq)==type(0.1):
            #single epsilon value
            dfg_freq_new[key] = dfg_freq[key]+abs(laplace.rvs(loc=0,scale=senstivity_freq/epsilon_freq,size=1)[0])
        else:
            #multiple epsilon value
            dfg_freq_new[key] = dfg_freq[key] + abs(laplace.rvs(loc=0, scale=senstivity_freq / epsilon_freq[key], size=1)[0])

    return dfg_freq_new


def differential_privacy_with_accuracy( dfg_freq, dfg_time,precision, distance,aggregate_type=AggregateType.SUM):
    #calculate epsilon and delta for  freq
    # epsilon_freq, delta_freq=calculate_epsilon_from_distance_freq(dfg_freq,  distance)
    epsilon_freq, delta_freq_dfg , delta_freq = calculate_epsilon_from_distance_freq_percentage_distances(dfg_freq, distance)

    # calculate epsilon and delta for  time

    epsilon_time, delta_time, delta_time_dfg = calculate_epsilon_from_distance_time_percentage_distance(dfg_time, distance, precision,aggregate_type)
    #  apply laplace noise and return the noisfied version of the DFG.

    # adding laplace noise to DFG freq
    dfg_freq_new = add_laplace_noise_freq(dfg_freq, epsilon_freq)

    # adding laplace noise to DFG time
    dfg_time, dfg_time_new = add_laplace_noise_time(aggregate_type, dfg_time, epsilon_time)

    return dfg_freq_new, dfg_time_new, epsilon_freq, epsilon_time, delta_freq , delta_time , delta_freq_dfg, delta_time_dfg

def differential_privacy_with_accuracy( dfg,precision, distance,aggregate_type=AggregateType.FREQ):
    #calculate epsilon and delta for  freq
    # epsilon_freq, delta_freq=calculate_epsilon_from_distance_freq(dfg_freq,  distance)

    if aggregate_type==AggregateType.FREQ:

        epsilon, delta_dfg , delta = calculate_epsilon_from_distance_freq_percentage_distances(dfg, distance)
        # adding laplace noise to DFG freq
        dfg_new = add_laplace_noise_freq(dfg, epsilon)
        return dfg_new, epsilon, delta, delta_dfg
    else:

        epsilon, delta, delta_dfg,delta_per_event = calculate_epsilon_from_distance_time_percentage_distance(dfg,distance,precision,aggregate_type)

        # adding laplace noise to DFG time
        dfg, dfg_new = add_laplace_noise_time(aggregate_type, dfg, epsilon)

        return dfg_new, epsilon, delta , delta_dfg, delta_per_event

    return dfg_new, epsilon, delta, delta_dfg


def risk_pruning(dfg_freq, dfg_time, dfg_delta_freq, dfg_delta_time, risk_pruning):
    keys = list(dfg_freq.keys())
    for key in keys:
        if dfg_delta_freq[key]<risk_pruning or dfg_delta_time[key]<risk_pruning:
            del dfg_freq[key]
            del dfg_time[key]
            del dfg_delta_freq[key]
            del dfg_delta_time[key]

    return dfg_freq, dfg_time, dfg_delta_freq, dfg_delta_time