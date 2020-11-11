import pandas as pd
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.conversion.log.versions.to_dataframe import get_dataframe_from_event_stream
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.dfg import factory as dfg_factory
from reportlab import xrange

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

from amun.guessing_advantage import AggregateType
from amun.input_module import read_xes

import seaborn as sns, numpy as np
import matplotlib.pyplot as plt

import sys
def get_dfg_time(data_dir ,data):
    """
    Returns the DFG matrix as a dictionary of lists. The key is the pair of acitivities
    and the value is a list of values
    """
    prune_parameter_freq = 350
    prune_parameter_time = -1  # keep all
    # read the xes file
    if data in "BPIC14":
        # log = csv_importer.import_event_stream(os.path.join(data_dir, data + ".csv"))
        dataset = csv_import_adapter.import_dataframe_from_path(os.path.join(data_dir, data + ".csv"), sep=";")
        dataset['case:concept:name'] = dataset['Incident ID']
        dataset['time:timestamp'] = dataset['DateStamp']
        dataset['concept:name'] = dataset['IncidentActivity_Type']
        log = conversion_factory.apply(dataset)
    elif data == "Unrineweginfectie":
        dataset = csv_import_adapter.import_dataframe_from_path(os.path.join(data_dir, data + ".csv"), sep=",")
        dataset['case:concept:name'] = dataset['Patientnummer']
        dataset['time:timestamp'] = dataset['Starttijd']
        dataset['concept:name'] = dataset['Aciviteit']
        log = conversion_factory.apply(dataset)
    else:
        log = xes_import_factory.apply(os.path.join(data_dir, data + ".xes"))
        dataset = get_dataframe_from_event_stream(log)


    # taking only the complete event to avoid ambiuoutiy
    if data not in ["BPIC13","BPIC20","BPIC19","BPIC14","Unrineweginfectie"]:
        dataset=dataset.where((dataset["lifecycle:transition"].str.upper()=="COMPLETE" ) )
        dataset=dataset.dropna(subset=['lifecycle:transition'])
    #moving first row to the last one
    temp_row= dataset.iloc[0]
    dataset2=dataset.copy()
    dataset2.drop(dataset2.index[0], inplace=True)
    dataset2=dataset2.append(temp_row)

    #changing column names
    columns= dataset2.columns
    columns= [i+"_2" for i in columns]
    dataset2.columns=columns

    #combining the two dataframes into one
    dataset = dataset.reset_index()
    dataset2=dataset2.reset_index()
    dataset=pd.concat([dataset, dataset2], axis=1)

    #filter the rows with the same case
    dataset=dataset[dataset['case:concept:name'] == dataset['case:concept:name_2']]

    #calculating time difference
    dataset['time:timestamp']=pd.to_datetime(dataset['time:timestamp'],utc=True)
    dataset['time:timestamp_2'] = pd.to_datetime(dataset['time:timestamp_2'],utc=True)

    # dataset['difference'] = (dataset['time:timestamp_2'] - dataset['time:timestamp']).astype(
    #     'timedelta64[ms]')   # in m seconds
    dataset['difference'] = (dataset['time:timestamp_2'] - dataset['time:timestamp']).astype(
        'timedelta64[D]')  # in m seconds

    #reformating the data to build the dfg
    dataset=dataset.set_index(['concept:name', 'concept:name_2'])
    dataset=dataset[['difference']]
    dataset= dataset.to_dict('split')

    #building the dfg matrix as a dictionary of lists
    dfg_time={}
    for index, value in zip(dataset['index'], dataset['data']):
        if index in dfg_time.keys():
            dfg_time[index].append(value[0])
        else:
            dfg_time[index]=[value[0]]



    return dfg_time


def plot(data="Traffic"):
    input_data=data

    '''**********************'''
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path=r"C:\\Gamal Elkoumy\\PhD\\OneDrive - Tartu Ülikool\\Differential Privacy\\source code"
    process_model_dir=os.path.join(dir_path,"experiment_figures","process_models")
    data_dir =os.path.join(dir_path,"data")
    figures_dir=os.path.join(dir_path,'experiment_figures')
    log_dir=os.path.join(dir_path,'experiment_logs')

    data_distribution=get_dfg_time(data_dir,"Traffic")



    return data_distribution


temp=plot()
# temp.difference.astype('timedelta64[D]').hist()
# temp.difference=abs(temp.difference.astype('timedelta64[D]'))
# data_distribution=list(temp.difference)
# (temp.difference.astype('timedelta64[D]')/pd.Timedelta(days=3)).hist()
# fig=temp.difference.hist()
data_distribution = list(temp.values())
data_distribution = [item for sublist in data_distribution for item in sublist]
ax=sns.distplot(data_distribution,kde=False)
# ax.set_xscale('log')
ax.set_yscale('log')
plt.ylabel("Histogram") #epsilon
plt.xlabel("Execution Time (Days)") #delta
fig = plt.gcf()

plt.show()

fig.savefig("histogram_of_traffic.pdf")