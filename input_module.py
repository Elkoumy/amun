"""
This module implements the functionality of reading the input from the user. The following formats are supported:
    * DFG
    * XES
"""
import sys
import os
import pandas as pd
import time
from datetime import datetime
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.conversion.log.versions.to_dataframe import get_dataframe_from_event_stream
from pm4py.objects.log.exporter.csv import factory as csv_exporter
from pm4py.algo.discovery.dfg import factory as dfg_factory

# from pm4py.algo.discovery.dfg import algorithm as dfg_discovery


def read_xes(xes_file):
    #read the xes file
    log = xes_import_factory.apply(xes_file)
    data=get_dataframe_from_event_stream(log)
    dfg_freq = dfg_factory.apply(log,variant="frequency")
    dfg_time =get_dfg_time(data)
    return dfg_freq,dfg_time


def get_dfg_time(data):
    """
    Returns the DFG matrix as a dictionary of lists. The key is the pair of acitivities
    and the value is a list of values
    """

    # taking only the complete event to avoid ambiuoutiy
    data=data.where(data["lifecycle:transition"]=="complete")
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
    data2=data2.reset_index()
    data=pd.concat([data, data2], axis=1)

    #filter the rows with the same case
    data=data[data['case:concept:name'] == data['case:concept:name_2']]

    #calculating time difference
    data['time:timestamp']=pd.to_datetime(data['time:timestamp'],utc=True)
    data['time:timestamp_2'] = pd.to_datetime(data['time:timestamp_2'],utc=True)
    data['difference']= (data['time:timestamp_2']- data['time:timestamp']).astype('timedelta64[ms]')

    #reformating the data to build the dfg
    data=data.set_index(['concept:name', 'concept:name_2'])
    data=data[['difference']]
    data= data.to_dict('split')

    #building the dfg matrix as a dictionary of lists
    dfg_time={}
    for index, value in zip(data['index'], data['data']):
        if index in dfg_time.keys():
            dfg_time[index].append(value[0])
        else:
            dfg_time[index]=[value[0]]


    return dfg_time
