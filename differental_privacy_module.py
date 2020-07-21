"""
This module contains the implementation of guessing advantage to add the differential privacy.
The module should be able to retun the DFG after adding the noise.
The module has two main functionalities:
    * Take delta as input, then calculate both epsilon and accuracy correlated with it.
    * Take accuracy as input, then calculate both epsilon and the delta (risk) correlated with it.
"""
from guessing_advantage import calculate_epsilon_freq , calculate_epsilon_from_delta, calculate_epsilon_time, AggregateType
import diffprivlib.mechanisms as privacyMechanisms
import sys


def differential_privacy_with_risk( dfg_freq, dfg_time, delta, precision):
    """
    This method adds the differential privacy to the DFG of both time and frequencies.
        * It calculates the epsilon using the guessing advantage technique.
        * It adds laplace noise to the DFGs.
        * It calculates the distance resulted from the noise
    """
    accuracy=1
    # calculate epsilon
    epsilon_freq,senstivity_freq=calculate_epsilon_freq(dfg_freq,delta)
    epsilon_time,senstivity_time=calculate_epsilon_time(dfg_time,delta,precision, aggregate_type=AggregateType.SUM)

    #TODO fix the sign problem in epsilon values
    epsilon_freq=abs(epsilon_freq)


    # adding laplace noise to DFG frequencies
    laplace_mechanism = privacyMechanisms.LaplaceBoundedDomain()
    laplace_mechanism.set_sensitivity(senstivity_freq).set_bounds(0, sys.maxsize).set_epsilon(epsilon_freq)

    dfg_freq_new = dfg_freq
    for key in dfg_freq_new.keys():
        dfg_freq_new[key]= laplace_mechanism.randomise(dfg_freq_new[key])

    # adding laplace noise to DFG time
    #TODO Calculate accuracy

    return dfg_freq_new, dfg_time, epsilon_freq,epsilon_time, accuracy



def differential_privacy_with_accuracy( dfg_freq, dfg_time, accuracy):
    epsilon=1
    delta=1

    # TODO calculate epsilon

    # TODO adding laplace noise

    # TODO Calculate delta ( the risk)
    return dfg_freq, dfg_time, epsilon, delta