"""
This module will include the guessing advantage implementation.
"""
from math import log, exp

from enum import Enum
class AggregateType(Enum):
    SUM = 1
    AVG = 2
    MIN = 3
    MAX = 4


def calculate_epsilon_from_delta(dfg,delta):
    # we will eventually have different epsilons for frequency and for time
    # we can output two epsilons, or have two different functions
    # in any case, it is safe to take the minimum of these epsilons if DP interface takes only one

    #for frequencies, we have r = 1
    r = 1

    # TODO need to learn how to compute these things from dfg format
    # for times, we need to compute r as the maximum possible time between two subsequent events
    # we can get even better results if:
    #     1) we have event log instead of dfg
    #     2) we compute a diffrent epsilon for different edges of dfg
    # r = ....

    p = (1 - delta) / 2
    epsilon = - log(p / (1 - p) * (1 / (delta + p) - 1)) / log(exp(1)) * (1 / r)

    return epsilon

def calculate_epsilon_freq(dfg,delta):
    epsilon =0
    sens=1
    p=(1-delta)/2
    R_ij=1  # from the discussion with Alisa
    epsilon = -(log(  (1-p)/p * (1/(delta*p) -1)  )) /(R_ij)
    return epsilon, sens


def calculate_epsilon_time(dfg,delta, aggregate_type):
    epsilon =0
    sens=1
    n=1 # length of the database

    """ calculating sensitivity based on type of aggregate"""
    if aggregate_type== AggregateType.AVG:
        sens=1/n
    elif aggregate_type== AggregateType.MAX or aggregate_type== AggregateType.MIN or aggregate_type== AggregateType.SUM:
        sens=1
    else:
        assert "Wrong aggregate type"


    return epsilon , sens

def calculate_epsilon_per_pair(values, R_ij, presision):
    epsilon =0


    return epsilon

def calculate_epsilon_from_accuracy(dfg,accuracy):
    epsilon=0

    return epsilon


