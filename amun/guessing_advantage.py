"""
This module will include the guessing advantage implementation.
"""
from math import log, exp, sqrt, inf
from statistics import median
import time
from enum import Enum
from statsmodels.distributions.empirical_distribution import ECDF
import multiprocessing as mp
import swifter
import numpy as np
import pandas as pd
from itertools import repeat
# import amun.multiprocessing_helper_functions
# import concurrent.futures

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

    """************parallel by edge******************"""

    p = mp.Pool(mp.cpu_count())
    result = p.starmap(calculate_epsilon_per_pair, zip(dfg.values(), repeat(delta), repeat(precision)))

    p.close()
    p.join()

    epsilon = dict(zip(list(dfg.keys()), result))

    return epsilon, sens


def calculate_epsilon_time_parallel(dfg, delta, precision, aggregate_type):
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

    """************parallel by edge******************"""

    p = mp.Pool(mp.cpu_count())
    result = p.starmap(calculate_epsilon_per_pair_parallel, zip(dfg.values(), repeat(delta), repeat(precision)))
    epsilon = dict(zip(list(dfg.keys()), list(result)))
    p.close()
    p.join()


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

def calculate_epsilon_per_pair_parallel(values, delta, precision):
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

            # covering the case with risk less than or equal 1-p_k
            if not (round(1 - p_k, 2) <= delta):  # the round is for very small differences, like 0.050000000000000044
                eps = - log(p_k / (1.0 - p_k) * (1.0 / (delta + p_k) - 1.0)) / log(exp(1.0)) * (1.0 / R_ij)

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
    """************parallel by edge******************"""
    """ Current slurm Bottleneck"""
    p = mp.Pool(mp.cpu_count())
    result = p.starmap(epsilon_time_from_distance,
                       zip(dfg_time.values(), repeat(aggregate_type), repeat(beta), repeat(distance), repeat(precision),
                           repeat(sens_time)))

    p.close()
    p.join()

    delta_dfg = dict(zip(list(dfg_time.keys()), [x[0] for x in result]))

    keys = list(dfg_time.keys())
    for idx, res in enumerate(result):
        delta_edge, delta_per_event_inner, delta_time_inner, epsilon_time_inner = res
        key = keys[idx]
        epsilon_time[key] = epsilon_time_inner
        delta_time = delta_time + delta_time_inner
        delta_per_event_inner = list(map(lambda i: [key, i], delta_per_event_inner))
        delta_per_event = delta_per_event + delta_per_event_inner
        delta_dfg[key] = max(delta_edge)


    if len(delta_time) > 0:
        delta_time = max(delta_time)

    delta_time = median(delta_dfg.values())
    return epsilon_time, delta_time, delta_dfg, delta_per_event


def epsilon_time_from_distance(dfg_time_inner, aggregate_type, beta, distance,
                               precision, sens_time):
    delta_time_inner = []
    delta_edge = []
    delta_per_event = []
    R_ij = max(dfg_time_inner)
    r_ij = R_ij * precision
    accurate_result = 0
    # calculating the accurate result
    if aggregate_type == AggregateType.AVG:
        accurate_result = sum(dfg_time_inner) * 1.0 / len(dfg_time_inner)
    elif aggregate_type == AggregateType.SUM:
        accurate_result = sum(dfg_time_inner) * 1.0
    elif aggregate_type == AggregateType.MIN:
        accurate_result = min(dfg_time_inner) * 1.0
    elif aggregate_type == AggregateType.MAX:
        accurate_result = max(dfg_time_inner) * 1.0
    # in case of the time is instant, we set epsilon to avoid the error of division by zero
    if accurate_result == 0:
        epsilon_time_ij = 1
    else:
        distance_ij = accurate_result * distance  # hence distance is between 0 and 1
        #  calculate epsilon
        epsilon_time_ij = sens_time / distance_ij * log(1 / beta)
    epsilon_time_inner = epsilon_time_ij
    # fix the case of time is fixed
    flag = 1
    prev = dfg_time_inner[0]
    current = dfg_time_inner
    for t_k in dfg_time_inner:

        # fix the case of time is fixed
        if t_k != prev:
            flag = 0
        prev = t_k

        cdf = ECDF(dfg_time_inner)

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
        # delta_per_event.append([x, current_delta])
        delta_per_event.append(current_delta)  # *****************!!!!!!!!!!!! changed
        if current_delta != 0:
            delta_time_inner.append(current_delta)

    return delta_edge, delta_per_event, delta_time_inner, epsilon_time_inner


def calculate_epsilon_from_distance_freq_percentage_distances(dfg_freq, distance_percentage):
    beta = 0.01
    sens_freq = 1
    # for frequencies, we have r = 1
    r_freq = 1
    delta_dfg = {}
    epsilon_dfg = {}

    p = mp.Pool(mp.cpu_count())
    result = p.starmap(epsilon_freq_from_distance,
                       zip(dfg_freq.values(), repeat(beta), repeat(distance_percentage), repeat(sens_freq)))
    p.close()
    p.join()

    delta_dfg = dict(zip(list(dfg_freq.keys()), [x[0] for x in result]))
    epsilon_dfg = dict(zip(list(dfg_freq.keys()), [x[1] for x in result]))

    delta_freq = max(list(delta_dfg.values()))

    return epsilon_dfg, delta_dfg, delta_freq


def epsilon_freq_from_distance(dfg_freq_inner, beta, distance_percentage, sens_freq):
    distance = distance_percentage * dfg_freq_inner
    epsilon_freq = sens_freq / distance * log(1 / beta)
    epsilon_dfg_inner = epsilon_freq
    #  Calculate delta ( the risk) from guessing advantage equation
    #  the following equation is validated by calculations
    delta_freq = (1 - sqrt(exp(- epsilon_freq))) / (1 + sqrt(exp(- epsilon_freq)))
    return delta_freq, epsilon_dfg_inner


def calculate_cdf_vectorized(data):
    cdf, val=data.relative_time_ecdf,data.val_plus
    cur_idx = 0
    for idx, i in enumerate(cdf.x[:-1]):
        if val > i:
            cur_idx += 1

            if val < cdf.x[idx + 1]:
                cur_idx -= 1
                break
    return cdf.y[cur_idx]
def estimate_epsilon_risk_vectorized(data, delta, precision):
    # NOTE: in the current version, there are no fixed time values.
    # Becuase the starting time now is being anonymized.

    data_state_max = data.groupby('state').relative_time.max()
    data_state_max['state'] = data_state_max.index

    # data= pd.merge(data, data_cdf, on=['state'], suffixes=("","_ecdf"))

    data = pd.merge(data, data_state_max, on=['state'], suffixes=("", "_max"))
    #calculate cdfs in vectorized manner
    data['r_ij']=data['relative_time_max']*precision
    data['val_plus']=data['relative_time'] + data['r_ij']
    data['val_minus'] = data['relative_time'] - data['r_ij']
    data.drop(['r_ij'], inplace=True, axis=1)
    # data['cdf_plus']=np.vectorize(calculate_cdf)(data.relative_time_ecdf,data.val_plus)
    # data['cdf_minus'] = np.vectorize(calculate_cdf)(data.relative_time_ecdf, data.val_minus)

    #optimize  calculate cdf function
    """
    CDF calculation using pandas 
    https://stackoverflow.com/questions/25577352/plotting-cdf-of-a-pandas-series-in-python
    """
    # data['cdf_plus'] = data[['relative_time_ecdf','val_plus']].swifter.apply(lambda x: calculate_cdf(x.relative_time_ecdf,x.val_plus),axis=1)
    # data['cdf_minus'] = data[['relative_time_ecdf', 'val_minus']].swifter.apply(
    #     lambda x: calculate_cdf(x.relative_time_ecdf, x.val_minus), axis=1)

    #state, relative_time
    stats_df = data.groupby(['state', 'relative_time'])['relative_time'].agg('count').pipe(pd.DataFrame).rename(
        columns={'relative_time': 'frequency'})
    # PDF
    stats_df['pdf'] = stats_df['frequency'] / stats_df.groupby(['state']).frequency.sum()
    # CDF
    stats_df['cdf'] = stats_df['pdf'].groupby(['state']).cumsum()
    stats_df = stats_df.reset_index()
    stats_df.drop(['pdf'], inplace=True, axis=1)


    #the plus_and_minus works like a value lookup
    plus_and_minus=data.groupby(['state', 'relative_time','val_plus','val_minus']).state.agg('count').pipe(pd.DataFrame)\
        .drop('state',axis=1)\
        .reset_index()


    #calculating CDF of the value + r_ij
    # temp = stats_df[['state', 'relative_time', 'cdf']].merge(plus_and_minus[['state', 'val_plus']], how='cross',
    #                                                 suffixes=("", "_right"))
    # temp = temp.loc[
    #     (temp.state == temp.state_right) & (temp.val_plus >= temp.relative_time), ['state','relative_time', 'val_plus', 'cdf']]\
    #     .groupby(['state', 'val_plus']).cdf.max().reset_index()


    stats_df=stats_df[['state', 'relative_time', 'cdf']]

    temp = stats_df.merge(plus_and_minus[['state', 'val_plus']], how='inner', on='state',
                                                             suffixes=("", "_right"))
    temp = temp.loc[(temp.val_plus >= temp.relative_time), ['state', 'relative_time', 'val_plus',
                                                                                   'cdf']] \
        .groupby(['state', 'val_plus']).cdf.max().reset_index()

    cdf_lookup=temp.merge(plus_and_minus[['state','relative_time', 'val_plus']], how='inner', on='state', suffixes=("","_right"))
    # print(cdf_lookup)
    cdf_lookup=cdf_lookup.loc[cdf_lookup.val_plus==cdf_lookup.val_plus_right,['state','relative_time','cdf']]

    cdf=cdf_lookup.rename(columns={'cdf':'cdf_plus'}) #holds the result
    # add the values to the dataframe
    data = data.merge(cdf, how='left', on=['state', 'relative_time'], suffixes=("", "_right"))
    data.drop(['val_plus'], inplace=True, axis=1)

    #calculate the CDF of the value - r_ij
    # temp = stats_df[['state', 'relative_time', 'cdf']].merge(plus_and_minus[['state', 'val_minus']], how='cross',
    #                                                          suffixes=("", "_right"))
    # temp = temp.loc[
    #     (temp.state == temp.state_right) & (temp.val_minus >= temp.relative_time), ['state', 'relative_time', 'val_minus',
    #                                                                                'cdf']] \
    #     .groupby(['state', 'val_minus']).cdf.max().reset_index()

    temp = stats_df.merge(plus_and_minus[['state', 'val_minus']], how='inner', on='state',
                                                             suffixes=("", "_right"))
    temp = temp.loc[(temp.val_minus >= temp.relative_time), ['state', 'relative_time',
                                                                                    'val_minus',
                                                                                    'cdf']] \
        .groupby(['state', 'val_minus']).cdf.max().reset_index()

    cdf_lookup = plus_and_minus[['state', 'relative_time', 'val_minus']].merge(temp, how='left', on='state',
                            suffixes=("", "_right"))

    cdf_lookup = cdf_lookup.loc[cdf_lookup.val_minus == cdf_lookup.val_minus_right, ['state', 'relative_time', 'cdf']]
    cdf_lookup=cdf_lookup.rename(columns={'cdf':'cdf_minus'})

    cdf = cdf_lookup.rename(columns={'cdf': 'cdf_minus'})  # holds the result

    # add the values to the dataframe
    data = data.merge(cdf, how='left', on=['state', 'relative_time'], suffixes=("", "_right"))

    # the minimum value of each distirubtion drops due to the condition "temp.val_minus >= temp.relative_time"
    # to fix that, we perform left join and replace the nans with zeros which means that the CDF of a value that is lower than
    # the minimum is zero
    data.cdf_minus=data.cdf_minus.fillna(0)


    # data= data.merge(cdf, how='left', on=['state','relative_time'], suffixes=("","_right"))
    # print(cdf[['state','relative_time']])
    # print(data.loc[data.cdf_plus.isna(), ['state','relative_time']])
    # data['cdf_minus'] = data[['relative_time_ecdf', 'val_minus']].swifter.apply(calculate_cdf_vectorized,axis=1)


    #calculate p_k in a vectorized manner
    data['p_k'] = data.cdf_plus - data.cdf_minus

    #calculate epsilon in a vectorized manner


    # data['eps'] = - np.log(data.p_k / (1.0 - data.p_k) * (1.0 / (delta + data.p_k) - 1.0))/ log(exp(1.0))* (1.0 / data.relative_time_max)

    data['eps'] = - np.log(data.p_k / (1.0 - data.p_k) * (1.0 / (delta + data.p_k) - 1.0))
    data['eps']=data['eps']/ log(exp(1.0))
    data['eps'] = data['eps']* (1.0 / data.relative_time_max.replace(0,-inf))

    #drop unused columns
    data.drop(['p_k','cdf_plus','cdf_minus','val_minus','relative_time_max'], inplace=True, axis=1)
    # data.drop('case:concept:name_linker',inplace=True,axis=1)

    # data['eps'] = data.swifter.apply(
    #     lambda x: estimate_epsilon_risk_dataframe(x['relative_time'], x['relative_time_ecdf'], x['relative_time_max'],
    #                                               delta, precision), axis=1)

    return data

def estimate_epsilon_risk_dataframe(val,cdf,R_ij,delta,precision):

    if cdf == 0:
        # case of a single item
        sens = 1.0
        p = (1.0 - delta) / 2.0
        R_ij = 1.0  # from the discussion with Alisa
        eps = - log(p / (1.0 - p) * (1.0 / (delta + p) - 1)) / log(exp(1.0)) * (1.0 / R_ij)

    else:
        if R_ij!=0:
            r_ij = R_ij * precision
            p_k = calculate_cdf(cdf, val + r_ij) - calculate_cdf(cdf, val - r_ij)
            if p_k + delta <1:
                eps = - log(p_k / (1.0 - p_k) * (1.0 / (delta + p_k) - 1.0)) / log(exp(1.0)) * (1.0 / R_ij)
            else:
                eps= inf
        else:
            eps=-inf

    return eps

def estimate_epsilon_risk_dataframe2(x):

    val, cdf, R_ij, delta, precision=x['relative_time'],x['relative_time_ecdf'],x['relative_time_max'], 0.2, 0.00000000001
    if cdf == 0:
        # case of a single item
        sens = 1.0
        p = (1.0 - delta) / 2.0
        R_ij = 1.0  # from the discussion with Alisa
        eps = - log(p / (1.0 - p) * (1.0 / (delta + p) - 1)) / log(exp(1.0)) * (1.0 / R_ij)

    else:
        if R_ij!=0:
            r_ij = R_ij * precision
            p_k = calculate_cdf(cdf, val + r_ij) - calculate_cdf(cdf, val - r_ij)
            if p_k + delta <1:
                eps = - log(p_k / (1.0 - p_k) * (1.0 / (delta + p_k) - 1.0)) / log(exp(1.0)) * (1.0 / R_ij)
            else:
                eps= inf
        else:
            eps=-inf

    return eps

def calculate_cdf_dataframe(val):
    if val.size>1:
        return ECDF(val)
    else:
        # in case of a single item
        return 0

