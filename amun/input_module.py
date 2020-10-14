"""
This module implements the functionality of reading the input from the user. The following formats are supported:
    * DFG
    * XES
"""
import pandas as pd
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.conversion.log.versions.to_dataframe import get_dataframe_from_event_stream
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.dfg import factory as dfg_factory

from amun.edges_pruning import pruning_by_edge_name_freq, pruning_by_edge_name_time
from amun.guessing_advantage import AggregateType
from math import log10
import os

# from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.algo.filtering.log.start_activities import start_activities_filter
from pm4py.algo.filtering.log.end_activities import end_activities_filter
from pm4py.objects.log.importer.csv import factory as csv_importer
from pm4py.objects.conversion.log import factory as conversion_factory
from pm4py.objects.log.adapters.pandas import csv_import_adapter

# from pruning_edges import get_pruning_edges


def read_xes(data_dir,dataset,aggregate_type,mode="pruning"):
    prune_parameter_freq=350
    prune_parameter_time=-1 #keep all
    #read the xes file
    if dataset in "BPIC14":
        # log = csv_importer.import_event_stream(os.path.join(data_dir, dataset + ".csv"))
        data = csv_import_adapter.import_dataframe_from_path(os.path.join(data_dir, dataset + ".csv"), sep=";")
        data['case:concept:name']=data['Incident ID']
        data['time:timestamp']= data['DateStamp']
        data['concept:name']= data['IncidentActivity_Type']
        log = conversion_factory.apply(data)
    elif dataset=="Unrineweginfectie":
        data = csv_import_adapter.import_dataframe_from_path(os.path.join(data_dir, dataset + ".csv"), sep=",")
        data['case:concept:name'] = data['Patientnummer']
        data['time:timestamp'] = data['Starttijd']
        data['concept:name'] = data['Aciviteit']
        log = conversion_factory.apply(data)
    else:
        log = xes_import_factory.apply(os.path.join(data_dir, dataset + ".xes"))
        data = get_dataframe_from_event_stream(log)




    # dataframe = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)
    dfg_freq = dfg_factory.apply(log,variant="frequency")
    dfg_time =get_dfg_time(data,aggregate_type,dataset)

    # pruning by values of freq and time
    # dfg_freq,dfg_time = frequency_pruning(dfg_freq,dfg_time, prune_parameter_freq, prune_parameter_time)
    if mode=="pruning":
        # pruning by 10% freq from apromore
        dfg_freq,dfg_time1= pruning_by_edge_name_freq(dfg_freq.copy(), dfg_time.copy(), dataset)
        #
        # pruning by 10% time from apromore
        dfg_freq2, dfg_time = pruning_by_edge_name_time(dfg_freq.copy(), dfg_time.copy(), dataset)


    """Getting Start and End activities"""
    # log = xes_importer.import_log(xes_file)
    log_start = start_activities_filter.get_start_activities(log)
    log_end= end_activities_filter.get_end_activities(log)
    return dfg_freq,dfg_time


def get_dfg_time(data,aggregate_type,dataset):
    """
    Returns the DFG matrix as a dictionary of lists. The key is the pair of acitivities
    and the value is a list of values
    """

    # taking only the complete event to avoid ambiuoutiy
    if dataset not in ["BPIC13","BPIC20","BPIC19","BPIC14","Unrineweginfectie"]:
        data=data.where((data["lifecycle:transition"].str.upper()=="COMPLETE" ) )
        data=data.dropna(subset=['lifecycle:transition'])
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
        'timedelta64[ms]')   # in m seconds

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

    dfg_time,units=converting_time_unit(dfg_time,aggregate_type)

    return dfg_time



def converting_time_unit(dfg_time, aggregate_type):
    unit = "mseconds"
    multiplier=1.0
    units={}
    for x in dfg_time.keys():

        # if for aggregate_type here
        if aggregate_type== AggregateType.AVG:
            accurate_result= abs(sum(dfg_time[x])*1.0 / len(dfg_time[x]))
        elif aggregate_type== AggregateType.SUM:
            accurate_result=  abs(sum(dfg_time[x])*1.0)
        elif aggregate_type== AggregateType.MIN:
            accurate_result=  abs(min(dfg_time[x])*1.0)
        elif aggregate_type== AggregateType.MAX:
            accurate_result= abs( max(dfg_time[x])*1.0)

        if not(accurate_result==0):
            if int(log10(accurate_result))+1<=2:
                unit="mseconds"
                multiplier = 1.0
            elif int(log10(accurate_result/(1000)))+1<=2:
                unit="seconds"
                multiplier=1/1000.0
            elif  int(log10(accurate_result/(1000*60)))+1<=2:
                unit="minutes"
                multiplier=1/1000.0/60.0
            elif  int(log10(accurate_result/(1000*60*60)))+1<=2:
                unit="hours"
                multiplier=1/1000.0/60/60.0
            elif  int(log10(accurate_result/(1000*60*60*24)))+1<=2:
                unit="days"
                multiplier=1/1000.0/60/60/24.0
            elif  int(log10(accurate_result/(1000*60*60*24*7)))+1<=2:
                unit="weeks"
                multiplier=1/1000.0/60/60/24/7.0
            elif  int(log10(accurate_result/(1000*60*60*24*30)))+1<=2:
                unit="month"
                multiplier=1/1000.0/60/60/24/30.0
            else:
                unit="years"
                multiplier=1/1000.0/60/60/24/365.0

        units[x]=unit

        #converting the values

        for val in range(0,len(dfg_time[x])):
            dfg_time[x][val]= dfg_time[x][val] * multiplier

    return dfg_time, units



