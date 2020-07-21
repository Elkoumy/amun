"""
This module contains the implementation of guessing advantage to add the differential privacy.
The module should be able to retun the DFG after adding the noise.
The module has two main functionalities:
    * Take delta as input, then calculate both epsilon and accuracy correlated with it.
    * Take accuracy as input, then calculate both epsilon and the delta (risk) correlated with it.
"""

def differential_privacy( dfg_freq, dfg_time, delta, precision):
    epsilon=1
    accuracy=1
    #TODO calculate epsilon

    #TODO adding laplace noise

    #TODO Calculate accuracy
    return dfg_freq, dfg_time, epsilon, accuracy



def differential_privacy( dfg_freq, dfg_time, accuracy):
    epsilon=1
    delta=1

    # TODO calculate epsilon

    # TODO adding laplace noise

    # TODO Calculate delta ( the risk)
    return dfg_freq, dfg_time, epsilon, delta