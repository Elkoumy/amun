
import networkx as nx
import matplotlib.pyplot as plt
from dafsa_classes import DAFSA
from pm4py.statistics.traces.log.case_statistics import get_variant_statistics, Parameters
from pm4py.objects.log.adapters.pandas import csv_import_adapter
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.conversion.log.versions.to_dataframe import get_dataframe_from_event_stream
import os

import pandas as pd
import numpy as np

#
data_dir=r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\data"
dataset="temp"
# dataset="CCC19"
from input_module import xes_to_DAFSA
from guessing_advantage import  estimate_epsilon_risk_dataframe, calculate_cdf_dataframe
from statsmodels.distributions.empirical_distribution import ECDF

def propagate_DAFSA_noise(edges, edges_df,noise):

    not_anonymized= edges_df[edges_df.added_noise<noise]
    traces=[]
    while not_anonymized.shape[0]>0:

        #try to make it weighted regarding the needed noise
        picked_edge_idx=not_anonymized.sample()['idx'].iloc[0]
        picked_edge= edges[picked_edge_idx]
        path,edges_df=get_path(picked_edge,edges_df, noise)
        traces.append(path)
        #TODO: write code here to take the path and make duplication in the event log
        not_anonymized = edges_df[edges_df.added_noise < noise]
    return edges, traces

def get_path(picked_edge,edges_df, noise):
    path=[]
    x=picked_edge

    parent_state= picked_edge.parent
    target_state= picked_edge.node
    path.append([picked_edge.activity_name, picked_edge.node.node_id])

    #adding noise to the edge
    if picked_edge.added_noise==-1:
        ttt=1
        picked_edge.added_noise+=noise+1
        edges_df.loc[edges_df.idx==picked_edge.lookup_idx,"added_noise"]+=noise+1
    else:
        noise=noise-picked_edge.added_noise
        picked_edge.added_noise += noise
        edges_df.loc[edges_df.idx == picked_edge.lookup_idx, "added_noise"] += noise


    #backward till start
    parent_state.input_edges
    current_state= picked_edge.parent
    while not current_state.start:
        prev_state=current_state

        #finding next state that needs noise
        idx=0
        for edge in list(current_state.input_edges.values()):
            if edge.added_noise<noise:
                break
            else:
                idx+=1
        if idx >= len(list(current_state.input_edges.values())):
            idx=0

        current_edge = list(current_state.input_edges.keys())[idx]

        # edge= list(current_state.input_edges.values())[idx]


        if current_state.input_edges[current_edge].added_noise == -1:
            current_state.input_edges[current_edge].added_noise += noise + 1
            # edge.added_noise += noise + 1
            edges_df.loc[edges_df.idx == current_state.input_edges[current_edge].lookup_idx, "added_noise"] += noise + 1
        else:
            # edge.added_noise += noise
            current_state.input_edges[current_edge].added_noise += noise
            edges_df.loc[edges_df.idx == current_state.input_edges[current_edge].lookup_idx, "added_noise"] += noise

        path.append([current_edge, current_state.node_id])
        current_state = list(current_state.input_edges.values())[idx].parent

    path=list(reversed(path))

    #forward till end
    current_state = picked_edge.node
    while not current_state.final:
        prev_state = current_state

        #finding next state that needs noise
        idx=0
        for edge in list(current_state.edges.values()):
            if edge.added_noise<noise:
                break
            else:
                idx+=1
        if idx >= len(list(current_state.edges.values())):
            idx=0

        current_edge = list(current_state.edges.keys())[idx]

        edge = list(current_state.edges.values())[idx]



        if edge.added_noise == -1:
            edge.added_noise += noise + 1
            edges_df.loc[edges_df.idx == edge.lookup_idx, "added_noise"] += noise + 1
        else:
            edge.added_noise += noise
            edges_df.loc[edges_df.idx == edge.lookup_idx, "added_noise"] += noise

        path.append([current_edge, current_state.node_id])
        current_state = list(current_state.edges.values())[idx].node
    target_state.edges

    return path,edges_df


data, dafsa, dafsa_edges, dafsa_edges_df= xes_to_DAFSA(data_dir, dataset)

delta=0.2
precision =0.00000000001

data_cdf = data.groupby('state').relative_time.apply(calculate_cdf_dataframe)
data_cdf['state']=data_cdf.index

data_state_max=data.groupby('state').relative_time.max()
data_state_max['state']=data_state_max.index

data= pd.merge(data, data_cdf, on=['state'], suffixes=("","_ecdf"))

data= pd.merge(data, data_state_max, on=['state'], suffixes=("","_max"))

data['eps']=data.apply(lambda x: estimate_epsilon_risk_dataframe(x['relative_time'],x['relative_time_ecdf'],x['relative_time_max'], delta, precision), axis=1)

""" propagating the noise across the DAFSA graph for the frequency"""
noise=3
dafsa_edges, traces_to_duplicate=propagate_DAFSA_noise(dafsa_edges,dafsa_edges_df,noise)

print(data.eps)


# result=estimate_epsilon_risk(values, 0.2, 0.05)
# print(result)

