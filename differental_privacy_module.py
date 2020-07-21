"""
This module contains the implementation of guessing advantage to add the differential privacy.
The module should be able to retun the DFG after adding the noise.
The module has two main functionalities:
    * Take delta as input, then calculate both epsilon and accuracy correlated with it.
    * Take accuracy as input, then calculate both epsilon and the delta (risk) correlated with it.
"""
from guessing_advantage import calculate_epsilon_freq , calculate_epsilon_from_delta, calculate_epsilon_time, AggregateType
def differential_privacy_with_risk( dfg_freq, dfg_time, delta, precision):
    epsilon=1
    accuracy=1
    #TODO calculate epsilon
    epsilon_freq,senstivity=calculate_epsilon_freq(dfg_freq,delta)
    epsilon_time,senstivity=calculate_epsilon_time(dfg_time,delta,precision, aggregate_type=AggregateType.SUM)
    #TODO adding laplace noise

    #TODO Calculate accuracy

    return dfg_freq, dfg_time, epsilon_freq,epsilon_time, accuracy



def differential_privacy_with_accuracy( dfg_freq, dfg_time, accuracy):
    epsilon=1
    delta=1

    # TODO calculate epsilon

    # TODO adding laplace noise

    # TODO Calculate delta ( the risk)
    return dfg_freq, dfg_time, epsilon, delta