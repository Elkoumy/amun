
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
dataset="Sepsis"

from input_module import xes_to_DAFSA
from guessing_advantage import  estimate_epsilon_risk_dataframe, calculate_cdf_dataframe
from statsmodels.distributions.empirical_distribution import ECDF

data, dafsa, dafsa_edges= xes_to_DAFSA(data_dir, dataset)

delta=0.2
precision =0.00000000001

data_cdf = data.groupby('state').relative_time.apply(calculate_cdf_dataframe)
data_cdf['state']=data_cdf.index

data_state_max=data.groupby('state').relative_time.max()
data_state_max['state']=data_state_max.index

data= pd.merge(data, data_cdf, on=['state'], suffixes=("","_ecdf"))

data= pd.merge(data, data_state_max, on=['state'], suffixes=("","_max"))
# temp=data.apply(lambda x: estimate_epsilon_risk_dataframe(x['relative_time'],x['relative_time_ecdf'],x['relative_time_max'], delta, precision), axis=1)
data['eps']=data.apply(lambda x: estimate_epsilon_risk_dataframe(x['relative_time'],x['relative_time_ecdf'],x['relative_time_max'], delta, precision), axis=1)

temp=dafsa_edges[0].node.node_id

print(data.eps)


# result=estimate_epsilon_risk(values, 0.2, 0.05)
# print(result)

