"""
This module will include the guessing advantage implementation.
"""
from math import log, exp, sqrt, inf
from statistics import median
import time
from enum import Enum
from statsmodels.distributions.empirical_distribution import ECDF
import multiprocessing as mp
# import swifter
import numpy as np
import pandas as pd
from itertools import repeat
import os
import glob
import pickle
import gc
from scipy.stats import laplace
# import amun.multiprocessing_helper_functions
# import concurrent.futures
import math
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


def estimate_epsilon_risk_vectorized(data, delta, precision,tmp_dir):
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
    # print("fix memory part")
    #fixing memory issues
    data.to_pickle('data.p')
    del(data)
    # stats_df.to_pickle('stats_df.p')

    """   ********* Performing chunking join **********"""
    # we use chunks to avoid running out of memory for large event logs

    # stats_df.to_csv('stats_df.csv',index=False, header=True, float_format='%.15f', compression='gzip', encoding='utf-8')
    # stats_df_cols=stats_df.columns
    chunk_size=10000 # number of states per chunk
    #the problem is the first state all cases go through it.

    no_of_chunks, max_large_state=partitioning_df(stats_df,plus_and_minus,tmp_dir,chunk_size)
    # print("Partitioning Done")
    del(stats_df)
    del(plus_and_minus)

    gc.collect()

    chunck_join(no_of_chunks,max_large_state,tmp_dir)
    # del(plus_and_minus)
    #loading data back from hard disk
    data=pd.read_pickle('data.p')
    #appending cdf
    cdf=append_cdf(tmp_dir,1)

    # add the first cdf values to the dataframe
    data = data.merge(cdf, how='left', on=['state', 'relative_time'], suffixes=("", "_right"))
    data.drop(['val_plus'], inplace=True, axis=1)
    del(cdf)

    #appending cdf2
    cdf2=append_cdf(tmp_dir,2)
    # add the values to the dataframe
    data = data.merge(cdf2, how='left', on=['state', 'relative_time'], suffixes=("", "_right"))
    del(cdf2)
    # the minimum value of each distirubtion drops due to the condition "temp.val_minus >= temp.relative_time"
    # to fix that, we perform left join and replace the nans with zeros which means that the CDF of a value that is lower than
    # the minimum is zero
    data.cdf_minus=data.cdf_minus.fillna(0)
    # and the maximum is 1
    data.cdf_plus = data.cdf_plus.fillna(1)

    # print("Second CDF done")
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


def get_noise_case_variant(delta):
    p=(1-delta)/2.0
    eps=- np.log(p / (1.0 - p) * (1.0 / (delta + p) - 1.0))

    sens_time = 1
    noise = laplace.rvs(loc=0, scale=sens_time / eps, size=1)[0]
    noise = int(math.ceil(abs(noise)))
    print("case variant noise: %s"%(noise))
    return noise,eps

def normalize_relative_time(data):
    if data['relative_time_min']==data['relative_time_max']:
        #return 1 in case of equal values, that will help to extract the noise value later
        return 1

    return (data['relative_time']-data['relative_time_min'])/(data['relative_time_max']-data['relative_time_min'])


def match_vals(row, cumsum):
    # cdf=float(cumsum[cumsum.index==row['relative_time']])
    #cdf plus
    # val_plus= row['relative_time']+precision
    # group_cdf=cumsum.loc[(row['prev_state'], row['concept:name'], row['state']),['relative_time','cdf']]
    group_cdf = cumsum.loc[(row['prev_state'], row['concept:name'], row['state']),['cdf']]
    # t1 = group_cdf.loc[group_cdf.index <= row['val_plus']]
    # cdf_plus=float(t1.iloc[-1][0])
    if row['val_plus']>=1:
        cdf_plus=1.0
    else:

        cdf_plus=group_cdf.loc[group_cdf.index <= row['val_plus']]
        cdf_plus = float(cdf_plus.iloc[-1][0])
        # cdf_plus=float(group_cdf[group_cdf.relative_time <= row['val_plus']].cdf.max())

    #cdf minus
    # val_minus = row['relative_time'] - precision
    if row['val_minus'] <= 0:
        cdf_minus = 0.0
    else:

        # query=group_cdf[group_cdf.relative_time <= row['val_minus']]
        query=group_cdf.loc[group_cdf.index <= row['val_minus']]
        if query.shape[0]==0:
            #in case the val_minus is lower than the minimum value but greater than zero
            cdf_minus=0
        else:
            cdf_minus = float(query.iloc[-1][0])

            # cdf_minus = float(query.cdf.max())
        # if cdf_minus==nan:
        #     cdf_minus===0


    return [ cdf_plus, cdf_minus]


def estimate_epsilon_risk_vectorized_with_normalization(data, delta, precision,tmp_dir):
    # NOTE: in the current version, there are no fixed time values.
    # Becuase the starting time now is being anonymized.

    # We estimate the min and max values for the normalization
    data['relative_time_max'] = data.groupby(['prev_state','concept:name','state'])['relative_time'].transform('max')

    data['relative_time_min'] = data.groupby(['prev_state','concept:name','state'])['relative_time'].transform('min')

    # perform normalization (scaling the values between 0 and 1, we use min max method
    data['relative_time_original']=data['relative_time']
    data['relative_time']= data[['relative_time','relative_time_min', 'relative_time_max']].apply(normalize_relative_time, axis=1)


    data=estimate_P_k(data, delta,tmp_dir)

    #calculate epsilon in a vectorized manner
    # handle p_k+delta >1

    '''delete records with prior knowledge + delta >=1'''
    cases_to_delete = data.loc[data.p_k==1]['case:concept:name'].unique()
    data = data[~data['case:concept:name'].isin(cases_to_delete)]
    data = data.reset_index(drop=True)


    data = estimate_P_k(data, delta, tmp_dir)



    data['eps'] =data.apply(epsilon_vectorized_internal,delta=delta, axis=1)


    #drop unused columns
    # we keep the max and min to denormalize the values
    data.drop([ 'cdf_plus', 'cdf_minus', 'val_minus','val_plus'], inplace=True, axis=1)

    return data


def estimate_P_k(data, delta,tmp_dir):
    # calculate cdfs in vectorized manner
    """for the normalized input, the r_ij equals 1"""
    # The range became +/- precision as r_ij =1
    # data['val_plus']=data['relative_time'] + precision
    # data['val_minus'] = data['relative_time'] - precision
    """Estimate precision as one per unit time"""
    # precision = 10 * 1 *(data['relative_time_max'] - data['relative_time_min'])/ (
    #             data['relative_time_max'] - data['relative_time_min'])**2  # within 10 minutes and time unit is in minutes
    # #nans happens when max=min
    # precision = precision.fillna(0)

    data['precision'] = 10 * 1* (data['relative_time_max'] - data['relative_time_min']) / (data['relative_time_max'] - data['relative_time_min'])**2
    data.precision = data.precision.fillna(0)
    # precision >max becomes 1
    data['precision'].loc[data.precision > 1] = 1
    # normalize precision
    # precision = (precision - data['relative_time_min']) / (data['relative_time_max'] - data['relative_time_min'])
    # precision = (precision ) / (data['relative_time_max'] - data['relative_time_min'])



    data['val_plus'] = data['relative_time'] + data['precision']
    data['val_plus']=data.val_plus.replace(inf,1)
    data['val_plus'].loc[data.val_plus > 1] = 1

    data['val_minus'] = data['relative_time'] - data['precision']
    data['val_minus'] = data.val_minus.replace(-inf, 0)
    data['val_minus'].loc[data.val_minus<0]=0
    # #no cdf below zero, so we replace -ve values with zeros
    # # no cdf greater than 1, so we replace  values >1 with 1
    # optimize  calculate cdf function

    # start partitioning here
    data=estimate_CDF_paritioned(data, tmp_dir)


    # calculate p_k in a vectorized manner
    data['p_k'] = 0
    #  adding a fix to the case of fixed distrubtion
    data['p_k'] = data.apply(estimate_P_k_vectorized, delta=delta, axis=1)

    data.drop('original_index',inplace=True, axis=1)

    return data





def estimate_CDF_paritioned(data, tmp_dir, chunk_size = 1000):
    """ the first state for large files is very large. We split the first state in a separate file.
     Then all the other states are splitted into several files.
    """

    # stats_df.to_csv('stats_df.csv', index=False, header=True, float_format='%.15f', compression='gzip',
    #                 encoding='utf-8')
    data=data.reset_index()
    data=data.rename(columns={'index': 'original_index'})

    data.to_pickle(os.path.join(tmp_dir, 'data_df_all'))
    no_of_chunks, max_large_state = partition_eventlog(chunk_size, data, tmp_dir)
    del data
    # iterate over every partition
    cdf_plus, cdf_minus=estimate_CDF_with_partitioning(no_of_chunks, max_large_state, tmp_dir)



    # read data back from the pickle file
    data=pd.read_pickle(os.path.join(tmp_dir, 'data_df_all'))
    data['cdf_plus'] = cdf_plus
    data['cdf_minus'] = cdf_minus


    # return len(list(range(0, unique_states.shape[0], chunk_size)))  #number of chunks
    return data # number of chunks , max largest state


def partition_eventlog(chunk_size, data, tmp_dir):
    large_state_size=1000
    data.sort_values(['prev_state', 'concept:name', 'state'], ascending=True, inplace=True)
    # unique_states = stats_df.state.unique()
    # unique_states = data.groupby(['prev_state', 'concept:name', 'state']).size().reset_index().rename(
    #     columns={0: 'count'}).drop('count', axis=1)
    unique_states = data.groupby(['prev_state', 'concept:name', 'state']).original_index.apply(list)


    large_states = data.groupby(['prev_state', 'concept:name', 'state']).relative_time.count()

    # separating large states from the others
    small_states = list(large_states.loc[large_states <= large_state_size].index)

    large_states = large_states.reset_index().rename(columns={'relative_time': 'counts'})
    large_states = large_states[large_states.counts > large_state_size].reset_index()

    unique_states = unique_states.loc[small_states]
    # unique_states = unique_states.reset_index()
    # unique_states = unique_states.loc[small_states]
    unique_states=unique_states.reset_index()


    # ['prev_state', 'concept:name', 'state']
    curr_dir = os.getcwd()
    idx = 0
    """large state separately"""
    for index, row in large_states.iterrows():
        res = data.loc[(data.state == row['state']) & (data.prev_state == row['prev_state']) & (
                    data['concept:name'] == row['concept:name']), :]
        res.to_pickle(os.path.join(tmp_dir, 'data_df_%s' % (idx)))

        # row_id = unique_states.index[
        #     (unique_states.state == row['state']) & (unique_states.prev_state == row['prev_state']) & (
        #                 unique_states['concept:name'] == row['concept:name'])].tolist()[0]
        # unique_states.drop(row_id, axis=0, inplace=True)

        idx += 1
    """ splitting other states regularly"""
    max_index_of_large_states = idx
    # print("partition of large states is %s"%(max_index_of_large_states-1))
    for i in range(0, unique_states.shape[0], chunk_size):
        # print("Current Chunck is: %s" % (i))
        current_states = unique_states.loc[i:i + chunk_size-1,'original_index']
        current_states = current_states.apply(pd.Series).stack().reset_index(drop=True)
        # res = stats_df.loc[stats_df.state.isin(current_states), :]

        # res = data.iloc[current_states.index]
        current_states = current_states.astype('int32')
        res = data.loc[current_states]
        # res = data.iloc[current_states]
        res.to_pickle(os.path.join(tmp_dir, 'data_df_%s' % (idx)))
        # plus_and_minus.loc[plus_and_minus.state.isin(current_states), :]\
        #     .to_pickle(os.path.join( tmp_dir,'plus_and_minus_%s'%(idx)))

        idx += 1
    return idx, max_index_of_large_states


def estimate_CDF_with_partitioning(num_of_chunks, max_large_state, tmp_dir):

    cdf_plus_combined=pd.Series()
    cdf_minus_combined = pd.Series()
    cdf_plus_lst=[]
    for i in range(0,num_of_chunks):
        data=pd.read_pickle(os.path.join( tmp_dir, 'data_df_%s' % (i)))
        data=data[['original_index','prev_state', 'concept:name', 'state', 'relative_time','val_plus','val_minus']]
        #the first state is large, so we separate it from the others
        if i<max_large_state:
            #single state partitions
            cdf_minus, cdf_plus = estimate_CDF_per_partition_single_transition(data)
            # print("*")
            # chunk_merge_plus_single_large_state(stats_df,plus_and_minus,i,tmp_dir)
        else:
            #multiple states partitions
            cdf_minus, cdf_plus = estimate_CDF_per_partition(data)
            # chunk_merge_plus(stats_df,plus_and_minus,i,tmp_dir)

            # store the cdf and keep the same index as the the orignial data
        cdf_plus_combined= cdf_plus_combined.append(cdf_plus)
        cdf_minus_combined= cdf_minus_combined.append(cdf_minus)
        cdf_plus_lst.append(cdf_plus)


    return cdf_plus_combined, cdf_minus_combined


def estimate_CDF_per_partition(data):

    stats_df = data.groupby(['prev_state', 'concept:name', 'state', 'relative_time'])['relative_time'].agg(
        'count').pipe(pd.DataFrame).rename(
        columns={'relative_time': 'frequency'})
    # PDF
    stats_df['pdf'] = stats_df['frequency'] / stats_df.groupby(['prev_state', 'concept:name', 'state']).frequency.sum()
    """ CDF  plus"""
    stats_df['cdf'] = stats_df['pdf'].groupby(['prev_state', 'concept:name', 'state']).cumsum()
    temp = data[['prev_state', 'concept:name', 'state', 'relative_time', 'val_plus']]
    stats_df = stats_df[['cdf']]
    stats_df = stats_df.reset_index()
    temp = temp.merge(stats_df, how='inner', on=['prev_state', 'concept:name', 'state'],
                      suffixes=("", "_right"))
    temp = temp.loc[temp.val_plus >= temp.relative_time_right]
    temp = temp.groupby(['prev_state', 'concept:name', 'state', 'relative_time', 'val_plus']).cdf.max().reset_index()

    #reseting the data index to keep it the same after merge
    data=data.reset_index()
    t_join = data.merge(temp, on=['prev_state', 'concept:name', 'state', 'relative_time'], how='left')
    #reindexing the t_join dataframe with the original data index
    t_join=t_join.set_index('index')

    cdf_plus = t_join.cdf

    """CDF minus"""
    temp = data[['prev_state', 'concept:name', 'state', 'relative_time', 'val_minus']]
    temp = temp.merge(stats_df, how='inner', on=['prev_state', 'concept:name', 'state'],
                      suffixes=("", "_right"))
    # negative values
    temp.loc[temp.val_minus < 0, 'val_minus'] = 0
    temp = temp.loc[temp.val_minus >= temp.relative_time_right]
    temp = temp.groupby(['prev_state', 'concept:name', 'state', 'relative_time', 'val_minus']).cdf.max().reset_index()

    #reseting the data index to keep it the same after merge
    data=data.reset_index()

    t_join = data.merge(temp, on=['prev_state', 'concept:name', 'state', 'relative_time'], how='left')

    # reindexing the t_join dataframe with the original data index
    t_join = t_join.set_index('index')

    cdf_minus = t_join.cdf
    cdf_minus = cdf_minus.fillna(0)

    return cdf_minus, cdf_plus


# def estimate_CDF_per_partition_single_transition(data):
#     stats_df = data.groupby(['prev_state', 'concept:name', 'state', 'relative_time'])['relative_time'].agg(
#         'count').pipe(pd.DataFrame).rename(
#         columns={'relative_time': 'frequency'})
#     # stats_df = data.groupby(['relative_time'])['relative_time'].agg(
#     #     'count').pipe(pd.DataFrame).rename(
#     #     columns={'relative_time': 'frequency'})
#     # PDF
#     stats_df['pdf'] = stats_df['frequency'] / stats_df.groupby(['prev_state', 'concept:name', 'state']).frequency.sum()
#     # stats_df['pdf'] = stats_df['frequency'] / stats_df.frequency.sum()
#     """ CDF  plus"""
#     # stats_df['cdf'] = stats_df['pdf'].groupby(['prev_state', 'concept:name', 'state']).cumsum()
#     stats_df['cdf'] = stats_df['pdf'].cumsum()
#
#     temp = data[['prev_state', 'concept:name', 'state', 'relative_time', 'val_plus']]
#     stats_df = stats_df[['cdf']]
#     stats_df = stats_df.reset_index()
#
#     # fix the below error (memory)
#     temp = temp.merge(stats_df, how='inner', on=['prev_state', 'concept:name', 'state'],
#                       suffixes=("", "_right"))
#     temp = temp.loc[temp.val_plus >= temp.relative_time_right]
#     temp = temp.groupby(['prev_state', 'concept:name', 'state', 'relative_time', 'val_plus']).cdf.max().reset_index()
#
#     #reseting the data index to keep it the same after merge
#     data=data.reset_index()
#     t_join = data.merge(temp, on=['prev_state', 'concept:name', 'state', 'relative_time'], how='left')
#     #reindexing the t_join dataframe with the original data index
#     t_join=t_join.set_index('index')
#
#     cdf_plus = t_join.cdf
#
#     """CDF minus"""
#     temp = data[['prev_state', 'concept:name', 'state', 'relative_time', 'val_minus']]
#     temp = temp.merge(stats_df, how='inner', on=['prev_state', 'concept:name', 'state'],
#                       suffixes=("", "_right"))
#     # negative values
#     temp.loc[temp.val_minus < 0, 'val_minus'] = 0
#     temp = temp.loc[temp.val_minus >= temp.relative_time_right]
#     temp = temp.groupby(['prev_state', 'concept:name', 'state', 'relative_time', 'val_minus']).cdf.max().reset_index()
#
#     #reseting the data index to keep it the same after merge
#     data=data.reset_index()
#
#     t_join = data.merge(temp, on=['prev_state', 'concept:name', 'state', 'relative_time'], how='left')
#
#     # reindexing the t_join dataframe with the original data index
#     t_join = t_join.set_index('index')
#
#     cdf_minus = t_join.cdf
#     cdf_minus = cdf_minus.fillna(0)
#
#     return cdf_minus, cdf_plus


def estimate_CDF_per_partition_single_transition(data):
    #here we don't need to group by 'prev_state', 'concept:name', 'state'


    stats_df = data.groupby(['prev_state', 'concept:name', 'state', 'relative_time'])['relative_time'].agg(
        'count').pipe(pd.DataFrame).rename(
        columns={'relative_time': 'frequency'})

    # PDF
    stats_df['pdf'] = stats_df['frequency'] / stats_df.groupby(['prev_state', 'concept:name', 'state']).frequency.sum()
    stats_df['cdf'] = stats_df['pdf'].groupby(['prev_state', 'concept:name', 'state']).cumsum()
    stats_df = stats_df[['cdf']]
    stats_df = stats_df.reset_index()

    cdf_plus = cdf_plus_single_state(data, stats_df)

    cdf_minus = cdf_minus_single_state(data, stats_df)

    return cdf_minus, cdf_plus


def cdf_minus_single_state(data, stats_df):
    """CDF minus"""
    temp = data[['original_index','prev_state', 'concept:name', 'state', 'relative_time', 'val_minus']]
    # negative values
    temp.loc[temp.val_minus < 0, 'val_minus'] = 0

    #todo: replicate the above.
    # temp = temp.merge(stats_df, how='inner', on=['prev_state', 'concept:name', 'state'],
    #                   suffixes=("", "_right"))
    # temp = temp.loc[temp.val_minus >= temp.relative_time_right]

    stats_df.state = stats_df.state.astype('int32')
    stats_df.prev_state = stats_df.prev_state.astype('int32')
    temp.sort_values('val_minus', inplace=True)
    stats_df.sort_values('relative_time', inplace=True)
    temp = pd.merge_asof(temp, stats_df, left_on='val_minus', right_on='relative_time',
                        # by=['prev_state', 'concept:name', 'state', 'relative_time'],
                        # direction="backward", tolerance=None,
                         suffixes=("", "_right"))

    temp = temp.groupby(['prev_state', 'concept:name', 'state', 'relative_time', 'val_minus']).cdf.max().reset_index()
    # reseting the data index to keep it the same after merge
    data = data.reset_index()
    t_join = data.merge(temp, on=['prev_state', 'concept:name', 'state', 'relative_time'], how='left')
    # reindexing the t_join dataframe with the original data index
    t_join = t_join.set_index('original_index')
    cdf_minus = t_join.cdf
    cdf_minus = cdf_minus.fillna(0)
    return cdf_minus


def cdf_plus_single_state(data, stats_df):
    """ CDF  plus"""
    temp = data[['original_index','prev_state', 'concept:name', 'state', 'relative_time', 'val_plus']]

    # TODO: reduce the size used by the following merge
    # temp = temp.merge(stats_df, how='inner', on=['prev_state', 'concept:name', 'state'],
    #                   suffixes=("", "_right"))
    # temp = temp.loc[temp.val_plus >= temp.relative_time_right]


    stats_df.state = stats_df.state.astype('int32')
    stats_df.prev_state = stats_df.prev_state.astype('int32')
    temp.sort_values('val_plus', inplace=True)
    stats_df.sort_values('relative_time', inplace=True)
    temp=pd.merge_asof(temp,stats_df,left_on='val_plus', right_on='relative_time', #by=['prev_state', 'concept:name', 'state', 'relative_time'],
                         # direction="backward", tolerance=None,
                         suffixes=("", "_right"))



    temp = temp.groupby(['prev_state', 'concept:name', 'state', 'relative_time', 'val_plus']).cdf.max().reset_index()
    # reseting the data index to keep it the same after merge
    data = data.reset_index()
    t_join = data.merge(temp, on=['prev_state', 'concept:name', 'state', 'relative_time'], how='left')
    # reindexing the t_join dataframe with the original data index
    t_join = t_join.set_index('original_index')
    cdf_plus = t_join.cdf
    return cdf_plus


def estimate_P_k_vectorized(data,delta):

    if data.relative_time_max==data.relative_time_min:
        #in case of fixed distribution, use the worst case scenario
        return (1-delta)/2

    return data.cdf_plus - data.cdf_minus


def epsilon_vectorized_internal(data, delta):
    if data.p_k+delta >=1:
        #in case p_k+delta>1, set epsilon = 0.5
        return 0.7

    if data.p_k==0:
        #in case of cdf_plus == cdf_minus, the epsilon will be inf
        # we set epsilon to 10 at that case.
        return 10
    # r =1 because of normalization
    return (- np.log(data.p_k / (1.0 - data.p_k) * (1.0 / (delta + data.p_k) - 1.0)))

def partitioning_df(stats_df,plus_and_minus,tmp_dir,chunk_size = 1000):
    """ the first state for large files is very large. We split the first state in a separate file.
     Then all the other states are splitted into several files.
    """


    # stats_df.to_csv('stats_df.csv', index=False, header=True, float_format='%.15f', compression='gzip',
    #                 encoding='utf-8')

    stats_df.sort_values(['prev_state','concept:name','state'], ascending=True, inplace=True)
    plus_and_minus.sort_values(['prev_state','concept:name','state'], ascending=True, inplace=True)
    # unique_states = stats_df.state.unique()
    unique_states = stats_df.groupby(['prev_state','concept:name','state']).size().reset_index().rename(columns={0:'count'}).drop('count',axis=1)
    large_states=stats_df.groupby(['prev_state','concept:name','state']).relative_time.count()

    #separating large states from the others
    large_states=large_states[large_states>1000].reset_index()

    #['prev_state', 'concept:name', 'state']
    curr_dir = os.getcwd()
    idx=0


    """large state separately"""
    for index,row in large_states.iterrows():
        res = stats_df.loc[(stats_df.state==row['state']) & (stats_df.prev_state==row['prev_state']) & (stats_df['concept:name']==row['concept:name']), :]
        res.to_pickle(os.path.join( tmp_dir, 'stats_df_%s' % (idx)))
        plus_and_minus.loc[ (plus_and_minus.state==row['state']) & (plus_and_minus.prev_state==row['prev_state']) & (plus_and_minus['concept:name']==row['concept:name']), :] \
            .to_pickle(os.path.join( tmp_dir, 'plus_and_minus_%s' % (idx)))
        # unique_states=unique_states[unique_states!=current_state]
        row_id=unique_states.index[ (unique_states.state==row['state'] )& (unique_states.prev_state==row['prev_state']) & (unique_states['concept:name']==row['concept:name'])].tolist()[0]
        unique_states.drop(row_id, axis=0,inplace=True)


        idx += 1

    """ splitting other states regularly"""

    max_index_of_large_states=idx
    # print("partition of large states is %s"%(max_index_of_large_states-1))
    for i in range(0, unique_states.shape[0], chunk_size):
        # print("Current Chunck is: %s" % (i))
        current_states = unique_states[i:i + chunk_size]
        # res = stats_df.loc[stats_df.state.isin(current_states), :]
        res = stats_df.iloc[current_states.index]
        res.to_pickle(os.path.join( tmp_dir,'stats_df_%s'%(idx)))
        # plus_and_minus.loc[plus_and_minus.state.isin(current_states), :]\
        #     .to_pickle(os.path.join( tmp_dir,'plus_and_minus_%s'%(idx)))
        plus_and_minus.iloc[current_states.index] \
            .to_pickle(os.path.join( tmp_dir, 'plus_and_minus_%s' % (idx)))
        idx+=1

    # return len(list(range(0, unique_states.shape[0], chunk_size)))  #number of chunks
    return idx , max_index_of_large_states # number of chunks , max largest state

def append_cdf(tmp_dir,num=1):
    cdf_name=0
    if num==1:
        cdf_name='cdf_*'
    else:
        cdf_name='cdf2_*'
    curr_dir = os.getcwd()
    # dir_path=os.path.join( tmp_dir,cdf_name)

    list_of_files = glob.glob(os.path.join( tmp_dir,cdf_name))

    cdf=[]
    for i in list_of_files:
        with open(i,'rb') as handle:
            cdf.append(pickle.load(handle))

    cdf=pd.concat(cdf)

    return cdf


def chunk_merge_plus(stats_df_chunk, plus_and_minus,idx,tmp_dir):


    stats_df_chunk = stats_df_chunk.merge(plus_and_minus, how='inner', on=['prev_state','concept:name','state'],
                              suffixes=("", "_right"))

    # plus_and_minus.columns = plus_and_minus.columns.map(lambda x: str(x) + '_right')
    # stats_df_chunk = stats_df_chunk.join(plus_and_minus, how='inner', rsuffix ="_right" )

    # df2=pd.merge(df1,x, left_on = "Colname1", right_on = "Colname2")
    # stats_df_chunk.to_csv("stats_df_chunk_merge.csv",mode="a",index=False,float_format='%.15f', compression='gzip', encoding='utf-8')

    #val_plus is from plus minus
    #relative_time is from stats_df
    stats_df_chunk = stats_df_chunk.loc[(stats_df_chunk.val_plus >= stats_df_chunk.relative_time), ['prev_state','concept:name','state', 'relative_time', 'val_plus',
                                                                            'cdf']] \
        .groupby(['prev_state','concept:name','state', 'val_plus']).cdf.max().reset_index()
    # print("performing second merge ")
    # stats_df_chunk = stats_df_chunk.merge(plus_and_minus, how='inner', on='state',
    #                             suffixes=("", "_right"))
    # # print(stats_df_chunk)
    # stats_df_chunk = stats_df_chunk.loc[stats_df_chunk.val_plus == stats_df_chunk.val_plus_right, ['state', 'relative_time', 'cdf']]
    stats_df_chunk = stats_df_chunk.merge(plus_and_minus, how='inner', on=['prev_state','concept:name','state', 'val_plus'],
                                          suffixes=("", "_right"))
    stats_df_chunk = stats_df_chunk.loc[:, ['prev_state','concept:name','state', 'relative_time', 'cdf']]
    cdf = stats_df_chunk.rename(columns={'cdf': 'cdf_plus'})  # holds the result
    curr_dir=os.getcwd()
    # os.makedirs(os.path.join(tmp_dir,'new%s'%(idx)))

    with open(os.path.join(tmp_dir,'cdf_%s.p'%(idx)), 'wb') as handle:
        pickle.dump(cdf, handle, protocol=pickle.HIGHEST_PROTOCOL)



def chunk_merge_minus(stats_df_chunk, plus_and_minus,idx,tmp_dir):
    stats_df_chunk = stats_df_chunk.merge(plus_and_minus[['prev_state','concept:name','state', 'val_minus']], how='inner', on=['prev_state','concept:name','state'],
                              suffixes=("", "_right"))
    # df2=pd.merge(df1,x, left_on = "Colname1", right_on = "Colname2")
    # stats_df_chunk.to_csv("stats_df_chunk_merge.csv",mode="a",index=False,float_format='%.15f', compression='gzip', encoding='utf-8')
    stats_df_chunk = stats_df_chunk.loc[(stats_df_chunk.val_minus >= stats_df_chunk.relative_time), ['prev_state','concept:name','state', 'relative_time', 'val_minus',
                                                                            'cdf']] \
        .groupby(['prev_state','concept:name','state', 'val_minus']).cdf.max().reset_index()
    # print("performing second merge ")
    stats_df_chunk = stats_df_chunk.merge(plus_and_minus, how='inner', on=['prev_state','concept:name','state', 'val_minus'],
                                          suffixes=("", "_right"))
    stats_df_chunk = stats_df_chunk.loc[:, ['prev_state','concept:name','state', 'relative_time', 'cdf']]

    # stats_df_chunk = stats_df_chunk.merge(plus_and_minus[['state', 'relative_time', 'val_minus']], how='inner', on='state',
    #                             suffixes=("", "_right"))
    # # print(stats_df_chunk)
    # stats_df_chunk = stats_df_chunk.loc[stats_df_chunk.val_minus == stats_df_chunk.val_minus_right, ['state', 'relative_time', 'cdf']]
    cdf2 = stats_df_chunk.rename(columns={'cdf': 'cdf_minus'})  # holds the result
    curr_dir=os.getcwd()
    # os.makedirs(os.path.join(tmp_dir,'new%s'%(idx)))
    # stats_df_chunk.to_pickle(os.path.join(tmp_dir,'new%s'%(idx),'stats_df_chunk_merge_%s.p'%(idx)))

    with open(os.path.join( tmp_dir, 'cdf2_%s.p' % (idx)), 'wb') as handle:
        pickle.dump(cdf2, handle, protocol=pickle.HIGHEST_PROTOCOL)


def chunk_merge_plus_single_large_state(stats_df_chunk, plus_and_minus,idx,tmp_dir):
    # print("idx is :%s"%(idx))
    # print("plus_and_minus.val_plus: %s"%(plus_and_minus.val_plus))
    # print("plus_and_minus.val_plus[0]: %s"%(plus_and_minus.val_plus.iloc[0]) )
    # print("plus_and_minus.relative_time[0]: %s" % (plus_and_minus.relative_time.iloc[0]))
    t = plus_and_minus.val_plus.iloc[0] - plus_and_minus.relative_time.iloc[0]  # the precision* max is the same for the same state

    stats_df_chunk.sort_values('relative_time', inplace=True)
    plus_and_minus.sort_values('val_plus', inplace=True)

    stats_df_chunk = pd.merge_asof(plus_and_minus, stats_df_chunk, left_on='val_plus', right_on='relative_time', by='state',
                         direction="backward", tolerance=t,
                         suffixes=("_right", ""))
    stats_df_chunk = stats_df_chunk[['state', 'relative_time', 'val_plus', 'cdf']].groupby(['state', 'val_plus']).cdf.max().reset_index()
    # print("*** first state done ***")


    # print("performing second merge ")
    stats_df_chunk = stats_df_chunk.merge(plus_and_minus, how='inner', on=['state','val_plus'],
                                          suffixes=("", "_right"))
    stats_df_chunk = stats_df_chunk.loc[:, ['state', 'relative_time', 'cdf']]
    # print("second merge done")

    cdf = stats_df_chunk.rename(columns={'cdf': 'cdf_plus'})  # holds the result
    curr_dir=os.getcwd()
    # os.makedirs(os.path.join(tmp_dir,'new%s'%(idx)))

    with open(os.path.join(tmp_dir,'cdf_%s.p'%(idx)), 'wb') as handle:
        pickle.dump(cdf, handle, protocol=pickle.HIGHEST_PROTOCOL)



def chunk_merge_minus_single_large_state(stats_df_chunk, plus_and_minus,idx,tmp_dir):

    t = plus_and_minus.val_plus.iloc[0] - plus_and_minus.relative_time.iloc[0]  # the precision* max is the same for the same state

    stats_df_chunk.sort_values('relative_time', inplace=True)
    plus_and_minus.sort_values('val_minus', inplace=True)

    stats_df_chunk = pd.merge_asof(plus_and_minus, stats_df_chunk, left_on='val_minus', right_on='relative_time', by='state',
                         direction="backward", tolerance=t,
                         suffixes=("_right", ""))
    stats_df_chunk = stats_df_chunk[['state', 'relative_time', 'val_minus', 'cdf']].groupby(['state', 'val_minus']).cdf.max().reset_index()
    # print("*** first state done ***")


    # print("performing second merge ")
    stats_df_chunk = stats_df_chunk.merge(plus_and_minus, how='inner', on=['state','val_minus'],
                                          suffixes=("", "_right"))
    stats_df_chunk = stats_df_chunk.loc[:, ['state', 'relative_time', 'cdf']]
    # print("second merge done")

    cdf2 = stats_df_chunk.rename(columns={'cdf': 'cdf_minus'})  # holds the result
    curr_dir = os.getcwd()
    # os.makedirs(os.path.join(tmp_dir,'new%s'%(idx)))
    # stats_df_chunk.to_pickle(os.path.join(tmp_dir,'new%s'%(idx),'stats_df_chunk_merge_%s.p'%(idx)))

    with open(os.path.join( tmp_dir, 'cdf2_%s.p' % (idx)), 'wb') as handle:
        pickle.dump(cdf2, handle, protocol=pickle.HIGHEST_PROTOCOL)

def chunck_join(num_of_chunks,max_large_state,tmp_dir):

    # print("performing first merge ")
    # stats_df = pd.read_csv('stats_df.csv', chunksize=chunksize, compression='gzip', encoding='utf-8')
    # [chunk_merge_plus(r, plus_and_minus, idx) for idx, r in enumerate(stats_df)]
    # with open('cdf.p','wb') as handle:
    #     pickle.dump(cdf, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # del(cdf)

    curr_dir = os.getcwd()


    for i in range(0,num_of_chunks):
        stats_df=pd.read_pickle(os.path.join( tmp_dir, 'stats_df_%s' % (i)))
        plus_and_minus = pd.read_pickle(os.path.join( tmp_dir, 'plus_and_minus_%s' % (i)))

        #the first state is large, so we separate it from the others
        if i<max_large_state:
            chunk_merge_plus_single_large_state(stats_df,plus_and_minus,i,tmp_dir)
        else:
            chunk_merge_plus(stats_df,plus_and_minus,i,tmp_dir)

    # print("plus merge done")

    # stats_df = pd.read_csv('stats_df.csv', chunksize=chunksize, compression='gzip', encoding='utf-8')
    # [chunk_merge_minus(r, plus_and_minus, idx) for idx, r in enumerate(stats_df)]

    for i in range(0,num_of_chunks):
        # print("current chunk id: %s"%(i))
        stats_df=pd.read_pickle(os.path.join( tmp_dir, 'stats_df_%s' % (i)))
        plus_and_minus = pd.read_pickle(os.path.join( tmp_dir, 'plus_and_minus_%s' % (i)))
        if i<max_large_state:
            chunk_merge_minus_single_large_state(stats_df,plus_and_minus,i,tmp_dir)
        else:
            chunk_merge_minus(stats_df,plus_and_minus,i,tmp_dir)



    # with open('cdf.p','rb') as handle:
    #     cdf=pickle.load(handle)
    # cdf=pd.concat(cdf)
    # cdf2=pd.concat(cdf2)


    # #removing temporary files
    # curr_dir = os.getcwd()
    # if os.path.exists(os.path.join(tmp_dir)):
    #     # os.rmdir(os.path.join(tmp_dir) )
    #     shutil.rmtree(os.path.join(tmp_dir), ignore_errors=True)
    # # if os.path.exists("stats_df_chunk_merge.csv"):
    # #     os.remove("stats_df_chunk_merge.csv")
    # os.makedirs(tmp_dir)

    # stats_df = stats_df.merge(plus_and_minus[['state', 'val_plus']], how='inner', on='state',
    #                                                          suffixes=("", "_right"))

    # stats_df = pd.read_csv('stats_df_chunk_merge.csv', compression='gzip', encoding='utf-8')
    # stats_df.columns=['state', 'relative_time','cdf','val_plus']
    # stats_df.state=stats_df.state.astype(int)
    # stats_df.relative_time = stats_df.relative_time.astype(float)
    # stats_df.cdf = stats_df.cdf.astype(float)
    # stats_df.val_plus = stats_df.val_plus.astype(float)

    #
    # stats_df = stats_df.loc[(stats_df.val_plus >= stats_df.relative_time), ['state', 'relative_time', 'val_plus',
    #                                                                         'cdf']] \
    #     .groupby(['state', 'val_plus']).cdf.max().reset_index()
    # print("performing second merge ")
    # cdf_lookup = stats_df.merge(plus_and_minus[['state', 'relative_time', 'val_plus']], how='inner', on='state',
    #                             suffixes=("", "_right"))
    # # print(cdf_lookup)
    # cdf_lookup = cdf_lookup.loc[cdf_lookup.val_plus == cdf_lookup.val_plus_right, ['state', 'relative_time', 'cdf']]
    # cdf = cdf_lookup.rename(columns={'cdf': 'cdf_plus'})  # holds the result
    # del (cdf_lookup)
    # del (stats_df)
    '''***********************'''

    # add the values to the dataframe
    # data = data.merge(cdf, how='left', on=['state', 'relative_time'], suffixes=("", "_right"))
    # data.drop(['val_plus'], inplace=True, axis=1)
    # calculate the CDF of the value - r_ij
    # temp = stats_df[['state', 'relative_time', 'cdf']].merge(plus_and_minus[['state', 'val_minus']], how='cross',
    #                                                          suffixes=("", "_right"))
    # temp = temp.loc[
    #     (temp.state == temp.state_right) & (temp.val_minus >= temp.relative_time), ['state', 'relative_time', 'val_minus',
    #                                                                                'cdf']] \
    #     .groupby(['state', 'val_minus']).cdf.max().reset_index()
    # stats_df = pd.read_csv('stats_df.csv')
    # # stats_df=pd.read_pickle('stats_df.p')
    # stats_df = stats_df.merge(plus_and_minus[['state', 'val_minus']], how='inner', on='state',
    #                           suffixes=("", "_right"))
    # stats_df = stats_df.loc[(stats_df.val_minus >= stats_df.relative_time), ['state', 'relative_time',
    #                                                                          'val_minus',
    #                                                                          'cdf']] \
    #     .groupby(['state', 'val_minus']).cdf.max().reset_index()
    # cdf_lookup = plus_and_minus[['state', 'relative_time', 'val_minus']].merge(stats_df, how='left', on='state',
    #                                                                            suffixes=("", "_right"))
    # cdf_lookup = cdf_lookup.loc[cdf_lookup.val_minus == cdf_lookup.val_minus_right, ['state', 'relative_time', 'cdf']]
    # cdf_lookup = cdf_lookup.rename(columns={'cdf': 'cdf_minus'})
    # cdf2 = cdf_lookup.rename(columns={'cdf': 'cdf_minus'})  # holds the result
    # del (cdf_lookup)
    # del (stats_df)




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

