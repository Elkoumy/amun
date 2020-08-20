"""
This module implements the functionality of reading the input from the user. The following formats are supported:
    * DFG
    * XES
"""
import pandas as pd
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.conversion.log.versions.to_dataframe import get_dataframe_from_event_stream
from pm4py.algo.discovery.dfg import factory as dfg_factory
from modules.guessing_advantage import AggregateType
from math import log10
# from pm4py.algo.discovery.dfg import algorithm as dfg_discovery


def read_xes(xes_file,aggregate_type):
    prune_parameter_freq=350
    prune_parameter_time=-1 #keep all
    #read the xes file
    log = xes_import_factory.apply(xes_file)
    data=get_dataframe_from_event_stream(log)
    dfg_freq = dfg_factory.apply(log,variant="frequency")
    dfg_time =get_dfg_time(data,aggregate_type)

    # pruning by values of freq and time
    dfg_freq,dfg_time = frequency_pruning(dfg_freq,dfg_time, prune_parameter_freq, prune_parameter_time)

    # pruning by 10% freq from apromore
    # dfg_freq,dfg_time=pruning_by_edge_name_freq(dfg_freq,dfg_time)

    # pruning by 10% time from apromore
    # dfg_freq, dfg_time = pruning_by_edge_name_time(dfg_freq, dfg_time)
    return dfg_freq,dfg_time


def get_dfg_time(data,aggregate_type):
    """
    Returns the DFG matrix as a dictionary of lists. The key is the pair of acitivities
    and the value is a list of values
    """

    # taking only the complete event to avoid ambiuoutiy
    data=data.where(data["lifecycle:transition"]=="complete")
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
    data2=data2.reset_index()
    data=pd.concat([data, data2], axis=1)

    #filter the rows with the same case
    data=data[data['case:concept:name'] == data['case:concept:name_2']]

    #calculating time difference
    data['time:timestamp']=pd.to_datetime(data['time:timestamp'],utc=True)
    data['time:timestamp_2'] = pd.to_datetime(data['time:timestamp_2'],utc=True)

    data['difference'] = (data['time:timestamp_2'] - data['time:timestamp']).astype(
        'timedelta64[ms]')   # in m seconds
    # data['difference']= (data['time:timestamp_2']- data['time:timestamp']).astype('timedelta64[ms]')/1000.0 # in seconds

    # data['difference']= (data['time:timestamp_2']- data['time:timestamp']).astype('timedelta64[ms]')/1000.0/60/60 # in hours

    # data['difference'] = (data['time:timestamp_2'] - data['time:timestamp']).astype('timedelta64[ms]') / 1000.0 / 60 / 60/24  # in days

    # data['difference'] = (data['time:timestamp_2'] - data['time:timestamp']).astype('timedelta64[ms]') / 1000.0 / 60 / 60/24 /7  # in weeks

    # data['difference'] = (data['time:timestamp_2'] - data['time:timestamp']).astype(
    #     'timedelta64[ms]') / 1000.0 / 60 / 60 / 24 /30  # in months

    # data['difference'] = (data['time:timestamp_2'] - data['time:timestamp']).astype(
    #     'timedelta64[ms]') / 1000.0 / 60 / 60 / 24 /365 # in years
    #making the time difference in seconds
    # data['difference'] = (data['time:timestamp_2'] - data['time:timestamp']).astype('timedelta64[s]')/60/60.0
    # making the time difference in minutes
    # data['difference'] = (data['time:timestamp_2'] - data['time:timestamp']).astype('timedelta64[m]')/60.0

    # making the time difference in hours
    # data['difference'] = (data['time:timestamp_2'] - data['time:timestamp']).astype('timedelta64[h]')

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
            accurate_result= sum(dfg_time[x])*1.0 / len(dfg_time[x])
        elif aggregate_type== AggregateType.SUM:
            accurate_result= sum(dfg_time[x])*1.0
        elif aggregate_type== AggregateType.MIN:
            accurate_result= min(dfg_time[x])*1.0
        elif aggregate_type== AggregateType.MAX:
            accurate_result= max(dfg_time[x])*1.0

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


def frequency_pruning(dfg_freq, dfg_time, prune_parameter_freq, prune_parameter_time):
    keys=list(dfg_freq.keys())
    for key in keys:
        if dfg_freq[key] < prune_parameter_freq:
            del dfg_freq[key]
            del dfg_time[key]
        else:
            values = dfg_time[key]
            for val in values:
                if val<=prune_parameter_time:
                    dfg_time[key].remove(val)
            if len(dfg_time[key])==0:
                del dfg_freq[key]
                del dfg_time[key]

    return dfg_freq, dfg_time


def pruning_by_edge_name_freq(dfg_freq, dfg_time):
    #in this method we implement the pruning by edge names kept by apromore
    #we keep 10% only

    freq_10=[('ER Registration','ER Triage')
,('ER Triage','ER Sepsis Triage')
,('ER Sepsis Triage','IV Liquid')
,('IV Liquid','IV Antibiotics')
,('IV Antibiotics','Admission NC')
,('IV Antibiotics','Admission IC')
,('Admission NC','Leucocytes')
,('Admission IC','LacticAcid')
,('LacticAcid','Leucocytes')
,('Leucocytes','CRP')
,('CRP','Release A')
,('CRP','Release B')
,('CRP','Release C')
,('CRP','Release D')
,('CRP','Release E')
,('Release A','Return ER')]

    keys = list(dfg_freq.keys())
    for key in keys:
        if key not in freq_10:
            del dfg_freq[key]
            del dfg_time[key]

    return dfg_freq, dfg_time

def pruning_by_edge_name_time(dfg_freq, dfg_time):
    # in this method we implement the pruning by edge names kept by apromore
    # we keep 10% only

    time_10 = [('IV Liquid','Release A')
,('Release A','Return ER')
,('LacticAcid','Release A')
,('IV Antibiotics','Release A')
,('Return ER','CRP')
,('Release D','Return ER')
,('Release C','Return ER')
,('CRP','Release B')
,('Release B','Admission NC')
,('Admission NC','Leucocytes')
,('Admission NC','LacticAcid')
,('Admission NC','Release C')
,('Admission NC','IV Antibiotics')
,('Admission NC','Release D')
,('Admission NC','ER Triage')
,('ER Sepsis Triage','Admission NC')
,('Admission IC','Admission NC')
,('Admission NC','ER Sepsis Triage')
,('ER Triage','ER Registration')
,('Leucocytes','Release E')
,('ER Registration','Admission IC')]

    keys = list(dfg_freq.keys())
    for key in keys:
        if key not in time_10:
            del dfg_freq[key]
            del dfg_time[key]

    return dfg_freq, dfg_time