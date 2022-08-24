from pm4py.objects.conversion.log.versions.to_dataframe import get_dataframe_from_event_stream
import pm4py
import pandas as pd
from scipy.stats import wasserstein_distance
import collections
import time

from amun.amun.guessing_advantage import AggregateType


def earth_mover_dist_freq(log1, log2):

    dfg1, start_activities, end_activities = pm4py.discover_dfg(log1)
    del log1
    dfg2, start_activities, end_activities = pm4py.discover_dfg(log2)
    del log2

    dic1=dict(dfg1)
    dic2=dict(dfg2)

    keys = set(list(dic1.keys()) + list(dic2.keys()))
    for key in keys:
        if key not in dic1.keys():
            dic1[key] = 0
        if key not in dic2.keys():
            dic2[key] = 0

    dic1 = collections.OrderedDict(sorted(dic1.items()))
    dic2 = collections.OrderedDict(sorted(dic2.items()))
    v1=list(dic1.values())
    v2=list(dic2.values())

    distance = wasserstein_distance(v1,v2)

    return distance


def earth_mover_dist_time(log1, log2):
    start = time.time()
    data = get_dataframe_from_event_stream(log1)
    dfg1= get_dfg_time(data)
    del log1
    del data

    data = get_dataframe_from_event_stream(log2)
    dfg2= get_dfg_time(data)
    del log2
    del data
    end = time.time()
    diff = end - start
    print("log to DFG : %s (minutes)" % (diff / 60.0))

    start=time.time()

    keys = set(list(dfg1.keys()) + list(dfg2.keys()))
    for key in keys:
        if key not in dfg1.keys():
            dfg1[key] = 0
        if key not in dfg2.keys():
            dfg2[key] = 0
    end = time.time()
    diff = end - start
    print("keys loop : %s (minutes)" % (diff / 60.0))


    dic1 = collections.OrderedDict(sorted(dfg1.items()))
    dic2 = collections.OrderedDict(sorted(dfg2.items()))
    v1=list(dic1.values())
    v2=list(dic2.values())

    start = time.time()
    distance = wasserstein_distance(v1,v2)
    end = time.time()
    diff = end - start
    print("wasserstein_distance : %s (minutes)" % (diff / 60.0))
    return distance


def get_dfg_time(data):
    """
    Returns the DFG matrix as a dictionary of lists. The key is the pair of acitivities
    and the value is a list of values
    """
    #moving first row to the last one
    temp_row= data.iloc[0]
    data2=data.copy()
    data2.drop(data2.index[0], inplace=True)
    data2=data2.append(temp_row)

    #changing column names
    columns= data2.columns
    columns= [i+"_2" for i in columns]
    data2.columns=columns

    #combining the two dataframes into one
    data = data.reset_index()
    data2=data2.reset_index()
    data=pd.concat([data, data2], axis=1)

    #filter the rows with the same case
    data=data[data['case:concept:name'] == data['case:concept:name_2']]

    #calculating time difference
    data['time:timestamp']=pd.to_datetime(data['time:timestamp'],utc=True)
    data['time:timestamp_2'] = pd.to_datetime(data['time:timestamp_2'],utc=True)

    data['difference'] = (data['time:timestamp_2'] - data['time:timestamp']).astype(
        'timedelta64[h]')   # in  hours

    #reformating the data to build the dfg
    data=data.set_index(['concept:name', 'concept:name_2'])
    data=data[['difference']]

    dfg_time=data.groupby(data.index).difference.sum()
    dfg_time=dfg_time.to_dict()


    return dfg_time

