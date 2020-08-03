"""
This module will include the guessing advantage implementation.
"""
from math import log, exp,sqrt,inf

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

    #  need to learn how to compute these things from dfg format
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

    epsilon = - log(p / (1.0 - p) * (1.0 / (delta + p) - 1)) / log(exp(1.0)) * (1.0 / R_ij)

    print("distance from the eq= "+str(sens/epsilon* log(1/0.05)))

    # print("Validation of the delta value")
    # delta_freq = (1 - sqrt(exp(-R_ij * epsilon))) / (1 + sqrt(exp(-R_ij * epsilon)))
    # print("for the input delta "+str(delta)+ "   the calculated epsilon is "+str(epsilon)+" the calculated delta  is "+str(delta_freq))
    # print("")
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


    flag=1
    prev=values[0]
    for i in values:
        if i != prev:
            flag=0
        prev = i

    if not flag:
        for t_k in values:
            p_k =calculate_cdf(cdf,t_k+r_ij)-calculate_cdf(cdf,t_k-r_ij)
            # eps = - log(p_k / (1.0 - p_k) * (1.0 / (delta + p_k) - 1.0))
            eps = - log(p_k / (1.0 - p_k) * (1.0 / (delta + p_k) - 1.0)) / log(exp(1.0)) * (1.0 / R_ij)
            # eps= -(log(  (1-p_k)/p_k * (1/(delta*p_k) -1)  )) /(R_ij)
            epsilons.append(eps)

        epsilon=min(epsilons)
    else:
        #  fix the ECDF when all the values are equal.
        # after the discussion, we decided to let the user know about that issue and maybe has can handle it on his own.
        epsilon=1
    return epsilon

def calculate_epsilon_from_distance_freq(dfg_freq, distance):
    beta = 0.05
    sens_freq = 1
    # for frequencies, we have r = 1
    r_freq = 1

    #  calculate epsilon
    epsilon_freq = sens_freq / distance * log(1 / beta)

    #  Calculate delta ( the risk) from guessing advantage equation
    #  the following equation is validated by calculations
    delta_freq = (1 - sqrt(exp(-r_freq * epsilon_freq))) / (1 + sqrt(exp(-r_freq * epsilon_freq)))

    return  epsilon_freq, delta_freq


def calculate_epsilon_from_distance_time( dfg_time, distance, aggregate_type=AggregateType.SUM):
    beta = 0.05

    # TODO update the below to reflect the new equation of delta for the time per time instance. Then take the maximum delta from all the instances.
    r_time=-inf
    for x in dfg_time.keys():
        if r_time<max(dfg_time[x]):
            r_time=max(dfg_time[x])

    sens_time = 1
    """ calculating sensitivity based on type of aggregate"""
    if aggregate_type == AggregateType.AVG:
        sens_time = 1 / len(dfg_time[0])
    elif aggregate_type == AggregateType.MAX or aggregate_type == AggregateType.MIN or aggregate_type == AggregateType.SUM:
        sens_time = 1
    else:
        assert "Wrong aggregate type"

    #  calculate epsilon
    # TODO update the equation to be calculated per instance first as p is different from frequency.
    epsilon_time = sens_time / distance * log(1 / beta)

    #  Calculate delta ( the risk) from guessing advantage equation

    delta_time = (1 - sqrt(exp(-r_time * epsilon_time))) / (1 + sqrt(exp(-r_time * epsilon_time)))


    return  epsilon_time,  delta_time


def calculate_cdf(cdf, val):

    cur_idx= 0
    for  idx,i in enumerate(cdf.x[:-1]):
        if val>i :
            cur_idx+=1

            if val <cdf.x[idx+1]:
                cur_idx-=1
    return cdf.y[cur_idx]
