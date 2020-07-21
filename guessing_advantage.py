"""
This module will include the guessing advantage implementation.
"""
from math import log, exp

from enum import Enum
from statsmodels.distributions.empirical_distribution import ECDF

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

    sens=1.0
    p=(1.0-delta)/2.0
    R_ij=1.0  # from the discussion with Alisa

    #TODO something wrong with the following equation. It returns negative numbers
    # epsilon = -(log(  (1-p)/p * (1/(delta*p) -1)  )) /(R_ij)
    epsilon = - log(p / (1.0 - p) * (1.0 / (delta + p) - 1)) / log(exp(1.0)) * (1.0 / R_ij)
    return epsilon, sens


def calculate_epsilon_time(dfg,delta,precision, aggregate_type):
    epsilon ={}
    sens=1
    n=1 # length of the database

    """ calculating sensitivity based on type of aggregate"""
    if aggregate_type== AggregateType.AVG:
        sens=1/n
    elif aggregate_type== AggregateType.MAX or aggregate_type== AggregateType.MIN or aggregate_type== AggregateType.SUM:
        sens=1
    else:
        assert "Wrong aggregate type"

    for x in dfg.keys():
        epsilon[x] = calculate_epsilon_per_pair(dfg[x],delta,precision)

    return epsilon , sens

def calculate_epsilon_per_pair(values,delta, precision):
    # values = [0.0, 0.2, .4, .6, .7, 10, 20, 100, 400, 500, 1000, 2000]
    values = sorted(values)
    R_ij=max(values)
    epsilons =[]
    r_ij=R_ij*precision
    cdf= ECDF(values)
    #TODO fix the ECDF when all the values are equal.
    for t_k in values:
        p_k =calculate_cdf(cdf,t_k+r_ij)-calculate_cdf(cdf,t_k-r_ij)
        eps = - log(p_k / (1.0 - p_k) * (1.0 / (delta + p_k) - 1.0))
        # eps = - log(p_k / (1.0 - p_k) * (1.0 / (delta + p_k) - 1.0)) / log(exp(1.0)) * (1.0 / R_ij)
        # eps= -(log(  (1-p_k)/p_k * (1/(delta*p_k) -1)  )) /(R_ij)
        epsilons.append(eps)

    epsilon=min(epsilons)

    return epsilon

def calculate_epsilon_from_accuracy(dfg,accuracy):
    epsilon=0

    return epsilon


def calculate_cdf(cdf, val):

    cur_idx= 0
    for  idx,i in enumerate(cdf.x[:-1]):
        if val>i :
            cur_idx+=1

            if val <cdf.x[idx+1]:
                cur_idx-=1
    return cdf.y[cur_idx]
