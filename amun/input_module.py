"""
This module implements the functionality of reading the input from the user. The following formats are supported:
    * DFG
    * XES
"""
import pandas as pd
import numpy as np
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.statistics.traces.log.case_statistics import get_variant_statistics
from pm4py.objects.conversion.log.versions.to_dataframe import get_dataframe_from_event_stream
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.dfg import factory as dfg_factory

# from amun.edges_pruning import pruning_by_edge_name_freq, pruning_by_edge_name_time
from amun.guessing_advantage import AggregateType
from math import log10
import os
from dafsa_classes import DAFSA

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
    # dfg_freq = dfg_factory.apply(log,variant="frequency")
    # dfg_time =get_dfg_time(data,aggregate_type,dataset)

    if aggregate_type==AggregateType.FREQ:
        dfg=dfg_factory.apply(log,variant="frequency")
    else:
        dfg = get_dfg_time(data, aggregate_type, dataset)



    """Getting Start and End activities"""
    # log = xes_importer.import_log(xes_file)
    log_start = start_activities_filter.get_start_activities(log)
    log_end= end_activities_filter.get_end_activities(log)
    # return dfg_freq,dfg_time
    return dfg



def xes_to_DAFSA(data_dir,dataset):
    """
     This function takes the XES file and returns:
        * DAFSA automata.
        * Event log as a dataframe annotated with states and contains the relative time.
    """
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
    elif dataset=="temp":
        data = csv_import_adapter.import_dataframe_from_path(os.path.join(data_dir, dataset + ".csv"), sep=",")
        log = conversion_factory.apply(data)
    else:
        log = xes_import_factory.apply(os.path.join(data_dir, dataset + ".xes"))
        data = get_dataframe_from_event_stream(log)

    if dataset not in ["BPIC13","BPIC20","BPIC19","BPIC14","Unrineweginfectie","temp"]:
        data=data.where((data["lifecycle:transition"].str.upper()=="COMPLETE" ) )
        data=data.dropna(subset=['lifecycle:transition'])

    log = conversion_factory.apply(data)


    ### Calculate relative time
    data=get_relative_time(data,dataset)
    ### Calculate DAFSA

    dafsa_log=get_DAFSA(log) # we pass the data as it is filtered from the lifecycle

    ### Anotate Event Log with DAFSA states
    data=annotate_eventlog_with_states(data,dafsa_log)

    # if aggregate_type==AggregateType.FREQ:
    #     dfg=dfg_factory.apply(log,variant="frequency")
    # else:
    #     dfg = get_dfg_time(data, aggregate_type, dataset)

    dafsa_edges,edges_df=get_edges(dafsa_log)


    return data,dafsa_log,dafsa_edges, edges_df

def get_edges(dafsa):
    edges=[]
    edges_df=[]
    edge_idx=0 #location within the lookup of edges (edges)
    for idx in dafsa.nodes:
        node=dafsa.nodes[idx]

        for edg_name in node.edges:
            #node.edges[edg_name].activity_name=edg_name
            node.edges[edg_name].state_id=idx
            node.edges[edg_name].lookup_idx=edge_idx
            node.edges[edg_name].activity_name=edg_name
            edges.append(node.edges[edg_name])

            edges_df.append([edge_idx,node.edges[edg_name].added_noise])
            edge_idx+=1

    edges_df=pd.DataFrame(edges_df,columns=['idx','added_noise'])
    return edges,edges_df

def get_relative_time(data, dataset):
    """
    Returns the event log with the relative time difference of every activity
    """
    # taking only the complete event to avoid ambiguoutiy
    if dataset not in ["BPIC13","BPIC20","BPIC19","BPIC14","Unrineweginfectie","temp"]:
        data=data.where((data["lifecycle:transition"].str.upper()=="COMPLETE" ) )
        data=data.dropna(subset=['lifecycle:transition'])

    #moving first row to the last one
    temp_row= data.iloc[0]
    data2=data.copy()
    # data2.drop(data2.index[0], inplace=True)
    # data2=data2.append(temp_row)
    # data2=pd.concat([pd.DataFrame(temp_row), data2], axis=1 ,ignore_index=True)
    # data2.reset_index(inplace=True)
    data2.loc[-1]=temp_row
    data2.index = data2.index + 1  # shifting index
    data2.sort_index(inplace=True)

    #changing column names
    columns= data2.columns
    columns= [i+"_2" for i in columns]
    data2.columns=columns

    #combining the two dataframes into one
    data = data[['case:concept:name', 'concept:name', 'time:timestamp']]
    data2 = data2[['case:concept:name_2', 'concept:name_2', 'time:timestamp_2']]

    data = data.reset_index()
    data2=data2.reset_index()
    data=pd.concat([data, data2], axis=1)



    #calculating time difference
    data['time:timestamp']=pd.to_datetime(data['time:timestamp'],utc=True)
    data['time:timestamp_2'] = pd.to_datetime(data['time:timestamp_2'],utc=True)

    # data['relative_time'] = (data['time:timestamp'] - data['time:timestamp_2']).astype(
    #     'timedelta64[ms]')   # in m seconds

    data['relative_time'] = (data['time:timestamp'] - data['time:timestamp_2']).astype(
        'timedelta64[h]')   # in  hours

    ''' In case of the first activity, we set the relative time to the unix epoch time
        to make it an integer. The anonymization of the start time of each trace       
    '''

    #set the relative time of the first activity of each case to zero
    # data.loc[data['case:concept:name'] != data['case:concept:name_2'],'relative_time']=0

    data.loc[0,'relative_time']= (data.loc[0]['time:timestamp'] - pd.Timestamp(
        "1970-01-01T00:00:00Z")) / pd.Timedelta('1s')

    data.loc[data['case:concept:name'] != data['case:concept:name_2'], 'relative_time'] = \
        (data.loc[data['case:concept:name'] !=data['case:concept:name_2'], 'time:timestamp'] - pd.Timestamp(
        "1970-01-01T00:00:00Z")) / pd.Timedelta('1s')




    # data.loc[data['case:concept:name'] != data['case:concept:name_2'], 'relative_time'] = \
    #     (data.loc[data['case:concept:name'] !=data['case:concept:name_2'], 'time:timestamp'] - data['time:timestamp'].min()
    #      ) / pd.Timedelta('1s')

    # pd.Timedelta(np.timedelta64(0, "ms"))
    #delete the last row as it is meaningless because data2 is longer by 1
    data.drop(data.tail(1).index, inplace=True)

    data=data[['case:concept:name','concept:name','time:timestamp','relative_time']]

    return data

def get_DAFSA(log):
    result = get_variant_statistics(log)
    traces = []
    for trace in result:
        current = trace['variant']  # separated by commas ','
        # current=current.replace(',',';')
        traces.append(current)

    # d= DAFSA(["tap", "taps", "top", "tops", "dibs"])

    dafsa_log = DAFSA(traces, delimiter=',')

    return dafsa_log

def annotate_eventlog_with_states(data,dafsa_log):
    states = []
    prev_state = 0
    curr_trace = -1
    curr_state=-1
    for idx, row in data.iterrows():
        if curr_trace != row['case:concept:name']:
            prev_state = 0
            curr_trace = row['case:concept:name']

        else:
            prev_state = curr_state
        temp=dafsa_log.lookup_nodes[prev_state]
        str='Acceptance of requests'
        str1=row['concept:name']
        t=str==str1
        curr_state = dafsa_log.lookup_nodes[prev_state].edges[row['concept:name']].node.node_id
        states.append(curr_state)

    data['state'] = states
    data.state = data.state.astype(int)

    return data

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



