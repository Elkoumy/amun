"""
This module will include the guessing advantage implementation.
"""
from math import log, exp, sqrt, inf
from statistics import median

from enum import Enum
from statsmodels.distributions.empirical_distribution import ECDF


class AggregateType(Enum):
    SUM = 1
    AVG = 2
    MIN = 3
    MAX = 4
    FREQ= 5


def calculate_epsilon_from_delta(dfg, delta):
    # we will eventually have different epsilons for frequency and for time
    # we can output two epsilons, or have two different functions
    # in any case, it is safe to take the minimum of these epsilons if DP interface takes only one

    # for frequencies, we have r = 1
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


def calculate_epsilon_freq(dfg, delta):
    sens = 1.0
    p = (1.0 - delta) / 2.0
    R_ij = 1.0  # from the discussion with Alisa

    epsilon = - log(p / (1.0 - p) * (1.0 / (delta + p) - 1)) / log(exp(1.0)) * (1.0 / R_ij)

    # print("distance from the eq= "+str(sens/epsilon* log(1/0.05)))

    # print("Validation of the delta value")
    # delta_freq = (1 - sqrt(exp(-R_ij * epsilon))) / (1 + sqrt(exp(-R_ij * epsilon)))
    # print("for the input delta "+str(delta)+ "   the calculated epsilon is "+str(epsilon)+" the calculated delta  is "+str(delta_freq))
    # print("")
    return epsilon, sens


def calculate_epsilon_time(dfg, delta, precision, aggregate_type):
    epsilon = {}
    sens = 1
    n = 1  # length of the database

    """ calculating sensitivity based on type of aggregate"""
    if aggregate_type == AggregateType.AVG:
        sens = 1 / n
    elif aggregate_type == AggregateType.MAX or aggregate_type == AggregateType.MIN or aggregate_type == AggregateType.SUM:
        sens = 1
    else:
        assert "Wrong aggregate type"

    for x in dfg.keys():
        epsilon[x] = calculate_epsilon_per_pair(dfg[x], delta, precision)

    return epsilon, sens


def calculate_epsilon_per_pair(values, delta, precision):
    # values = [0.0, 0.2, .4, .6, .7, 10, 20, 100, 400, 500, 1000, 2000]
    values =list(map(abs, values))
    values = sorted(values)
    R_ij = max(values)
    epsilons = []
    r_ij = R_ij * precision
    cdf = ECDF(values)

    epsilon = inf
    flag = 1
    prev = values[0]
    for i in values:
        if i != prev:
            flag = 0
        prev = i

    if not flag:
        for t_k in values:
            p_k = calculate_cdf(cdf, t_k + r_ij) - calculate_cdf(cdf, t_k - r_ij)
            # eps = - log(p_k / (1.0 - p_k) * (1.0 / (delta + p_k) - 1.0))
            # print("p_k="+str(p_k))
            # print("delta"+str(delta))
            # print("1-p_k"+str(1-p_k))
            # print("1-p_k<=delta"+str(1-p_k<=delta))
            # print("eps="+str(log(p_k / (1.0 - p_k) * (1.0 / (delta + p_k) - 1.0))))

            # covering the case with risk less than or equal 1-p_k
            if not (round(1 - p_k, 2) <= delta):  # the round is for very small differences, like 0.050000000000000044
                eps = - log(p_k / (1.0 - p_k) * (1.0 / (delta + p_k) - 1.0)) / log(exp(1.0)) * (1.0 / R_ij)
                # eps= -(log(  (1-p_k)/p_k * (1/(delta*p_k) -1)  )) /(R_ij)
                epsilons.append(eps)
            else:
                epsilons.append(inf)

        if len(epsilons) > 0:
            epsilon = min(epsilons)
    else:
        #  fix the ECDF when all the values are equal.
        # after the discussion, we decided to let the user know about that issue and maybe has can handle it on his own.
        # epsilon=-inf
        epsilon = inf
    return epsilon


def calculate_epsilon_from_distance_freq(dfg_freq, distance):
    beta = 0.01
    sens_freq = 1
    # for frequencies, we have r = 1
    r_freq = 1

    #  calculate epsilon
    epsilon_freq = sens_freq / distance * log(1 / beta)

    #  Calculate delta ( the risk) from guessing advantage equation
    #  the following equation is validated by calculations
    delta_freq = (1 - sqrt(exp(- epsilon_freq))) / (1 + sqrt(exp(- epsilon_freq)))

    return epsilon_freq, delta_freq


def calculate_epsilon_from_distance_time(dfg_time, distance, precision, aggregate_type=AggregateType.SUM):
    beta = 0.05

    # reflect the new equation of delta for the time per time instance. Then take the maximum delta from all the instances.
    sens_time = 1
    """ calculating sensitivity based on type of aggregate"""
    if aggregate_type == AggregateType.AVG:
        sens_time = 1 / len(dfg_time[0])
    elif aggregate_type == AggregateType.MAX or aggregate_type == AggregateType.MIN or aggregate_type == AggregateType.SUM:
        sens_time = 1
    else:
        assert "Wrong aggregate type"

    #  calculate epsilon
    # the equation to be calculated per instance first as p is different from frequency.
    epsilon_time = sens_time / distance * log(1 / beta)

    #  Calculate delta ( the risk) from guessing advantage equation
    delta_time = []
    delta_dfg = {}
    for x in dfg_time.keys():
        delta_edge = []
        R_ij = max(dfg_time[x])
        r_ij = R_ij * precision

        # fix the case of time is fixed
        flag = 1
        prev = dfg_time[x][0]
        current = dfg_time[x]
        for t_k in dfg_time[x]:

            # fix the case of time is fixed
            if t_k != prev:
                flag = 0
            prev = t_k

            cdf = ECDF(dfg_time[x])

            # p_k is calculated for every instance.
            cdf1 = calculate_cdf(cdf, t_k + r_ij)
            cdf2 = calculate_cdf(cdf, t_k - r_ij)
            p_k = cdf1 - cdf2

            # current_delta = p_k*( 1/(   (1-p_k) * exp(-R_ij * epsilon_time) +p_k) -1)
            current_delta = (p_k / ((1 - p_k) * exp(-R_ij * epsilon_time) + p_k)) - p_k
            # eps = - log(p_k / (1.0 - p_k) * (1.0 / (current_delta + p_k) - 1.0)) / log(exp(1.0)) * (1.0 / R_ij)
            # we append the deltas and take the maximum delta out of them
            # if current_delta != float.nan:
            delta_edge.append(current_delta)
            if current_delta != 0:
                delta_time.append(current_delta)

        delta_dfg[x] = max(delta_edge)
    if len(delta_time) > 0:
        delta_time = median(delta_time)

    delta_time = median(delta_dfg.values())
    return epsilon_time, delta_time, delta_dfg


def calculate_cdf(cdf, val):
    cur_idx = 0
    for idx, i in enumerate(cdf.x[:-1]):
        if val > i:
            cur_idx += 1

            if val < cdf.x[idx + 1]:
                cur_idx -= 1
                break
    return cdf.y[cur_idx]


def calculate_epsilon_from_distance_time_new_approach(dfg_time, distance, precision, aggregate_type=AggregateType.SUM):
    beta = 0.05

    # reflect the new equation of delta for the time per time instance. Then take the maximum delta from all the
    # instances.
    sens_time = 1
    """ calculating sensitivity based on type of aggregate"""
    if aggregate_type == AggregateType.AVG:
        sens_time = 1 / len(dfg_time[0])
    elif aggregate_type == AggregateType.MAX or aggregate_type == AggregateType.MIN or aggregate_type == AggregateType.SUM:
        sens_time = 1
    else:
        assert "Wrong aggregate type"

    # m is the number of edges

    m = len(dfg_time.keys())

    # calculating R among all the edges

    R = 0
    for x in dfg_time.keys():
        R = R + max(dfg_time[x])

    #  Calculate delta ( the risk) from guessing advantage equation
    delta_time = []
    delta_dfg = {}
    epsilon_time = {}
    for x in dfg_time.keys():
        delta_edge = []
        R_ij = max(dfg_time[x])
        r_ij = R_ij * precision

        #  calculate epsilon
        # the equation to be calculated per instance first as p is different from frequency.

        distance_ij = m * distance * exp(R_ij) / R
        # distance_ij = m * distance * R_ij / R

        epsilon_time_ij = sens_time / distance_ij * log(1 / beta)

        epsilon_time[x] = epsilon_time_ij
        # fix the case of time is fixed
        flag = 1
        prev = dfg_time[x][0]
        current = dfg_time[x]
        for t_k in dfg_time[x]:

            # fix the case of time is fixed
            if t_k != prev:
                flag = 0
            prev = t_k

            cdf = ECDF(dfg_time[x])

            # p_k is calculated for every instance.
            cdf1 = calculate_cdf(cdf, t_k + r_ij)
            cdf2 = calculate_cdf(cdf, t_k - r_ij)
            p_k = cdf1 - cdf2

            # current_delta = p_k*( 1/(   (1-p_k) * exp(-R_ij * epsilon_time) +p_k) -1)
            current_delta = (p_k / ((1 - p_k) * exp(-R_ij * epsilon_time_ij) + p_k)) - p_k
            # eps = - log(p_k / (1.0 - p_k) * (1.0 / (current_delta + p_k) - 1.0)) / log(exp(1.0)) * (1.0 / R_ij)
            # we append the deltas and take the maximum delta out of them
            # if current_delta != float.nan:
            delta_edge.append(current_delta)
            if current_delta != 0:
                delta_time.append(current_delta)

        delta_dfg[x] = max(delta_edge)
    if len(delta_time) > 0:
        delta_time = max(delta_time)

    delta_time=median(delta_dfg.values())
    return epsilon_time, delta_time, delta_dfg



def calculate_epsilon_from_distance_time_percentage_distance(dfg_time, distance, precision, aggregate_type=AggregateType.SUM):
    beta = 0.05

    # reflect the new equation of delta for the time per time instance. Then take the maximum delta from all the
    # instances.
    sens_time = 1
    """ calculating sensitivity based on type of aggregate"""
    if aggregate_type == AggregateType.AVG:
        sens_time = 1 / len(dfg_time.keys())
    elif aggregate_type == AggregateType.MAX or aggregate_type == AggregateType.MIN or aggregate_type == AggregateType.SUM:
        sens_time = 1
    else:
        assert "Wrong aggregate type"

    # m is the number of edges

    m = len(dfg_time.keys())

    # calculating R among all the edges

    R = 0
    for x in dfg_time.keys():
        R = R + max(dfg_time[x])

    #  Calculate delta ( the risk) from guessing advantage equation
    delta_time = []
    delta_dfg = {}
    epsilon_time = {}
    delta_per_event=[]
    for x in dfg_time.keys():
        delta_edge = []
        R_ij = max(dfg_time[x])
        r_ij = R_ij * precision

        accurate_result=0
        #calculating the accurate result
        if aggregate_type== AggregateType.AVG:
            accurate_result= sum(dfg_time[x])*1.0 / len(dfg_time[x])
        elif aggregate_type== AggregateType.SUM:
            accurate_result= sum(dfg_time[x])*1.0
        elif aggregate_type== AggregateType.MIN:
            accurate_result= min(dfg_time[x])*1.0
        elif aggregate_type== AggregateType.MAX:
            accurate_result= max(dfg_time[x])*1.0

        #in case of the time is instant, we set epsilon to avoid the error of division by zero
        if accurate_result==0:
            epsilon_time_ij=1
        else:
            distance_ij = accurate_result*distance # hence distance is between 0 and 1
            #  calculate epsilon
            epsilon_time_ij = sens_time / distance_ij * log(1 / beta)

        epsilon_time[x] = epsilon_time_ij
        # fix the case of time is fixed
        flag = 1
        prev = dfg_time[x][0]
        current = dfg_time[x]
        for t_k in dfg_time[x]:

            # fix the case of time is fixed
            if t_k != prev:
                flag = 0
            prev = t_k

            cdf = ECDF(dfg_time[x])

            # p_k is calculated for every instance.
            cdf1 = calculate_cdf(cdf, t_k + r_ij)
            cdf2 = calculate_cdf(cdf, t_k - r_ij)
            p_k = cdf1 - cdf2

            # current_delta = p_k*( 1/(   (1-p_k) * exp(-R_ij * epsilon_time) +p_k) -1)
            current_delta = (p_k / ((1 - p_k) * exp(-R_ij * epsilon_time_ij) + p_k)) - p_k
            # eps = - log(p_k / (1.0 - p_k) * (1.0 / (current_delta + p_k) - 1.0)) / log(exp(1.0)) * (1.0 / R_ij)
            # we append the deltas and take the maximum delta out of them
            # if current_delta != float.nan:
            delta_edge.append(current_delta)
            delta_per_event.append([x,current_delta])
            if current_delta != 0:
                delta_time.append(current_delta)
        delta_dfg[x] = max(delta_edge)
    if len(delta_time) > 0:
        delta_time = max(delta_time)

    delta_time=median(delta_dfg.values())
    return epsilon_time, delta_time, delta_dfg,delta_per_event


def calculate_epsilon_from_distance_freq_percentage_distances(dfg_freq, distance_percentage):
    beta = 0.01
    sens_freq = 1
    # for frequencies, we have r = 1
    r_freq = 1
    delta_dfg={}
    epsilon_dfg={}
    for x in dfg_freq.keys():
        #  calculate epsilon
        temp=dfg_freq[x]
        distance=distance_percentage* dfg_freq[x]
        epsilon_freq = sens_freq / distance * log(1 / beta)
        epsilon_dfg[x]=epsilon_freq
        #  Calculate delta ( the risk) from guessing advantage equation
        #  the following equation is validated by calculations
        delta_freq = (1 - sqrt(exp(- epsilon_freq))) / (1 + sqrt(exp(- epsilon_freq)))
        delta_dfg[x]=delta_freq

    delta_freq=max(list(delta_dfg.values()))
    return epsilon_dfg, delta_dfg, delta_freq