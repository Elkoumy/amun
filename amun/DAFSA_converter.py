
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
data= xes_to_DAFSA(data_dir, dataset)
#
# log = xes_import_factory.apply(os.path.join(data_dir, dataset + ".xes"))
# data = get_dataframe_from_event_stream(log)
# result= get_variant_statistics(log)
# traces=[]
# for trace in result:
#     current=trace['variant'] #separated by commas ','
#     # current=current.replace(',',';')
#     traces.append(current)
#
# # d= DAFSA(["tap", "taps", "top", "tops", "dibs"])
#
# dafsa_log= DAFSA(traces, delimiter=',')
#
# states=[]
# prev_state=0
# curr_trace= -1
# for idx, row in data.iterrows():
#     if curr_trace != row['case:concept:name']:
#         prev_state = 0
#         curr_trace = row['case:concept:name']
#
#     else:
#         prev_state = curr_state
#
#     curr_state = dafsa_log.lookup_nodes[prev_state].edges[row['concept:name']].node.node_id
#     states.append(curr_state)
#
# data['state']=states
# data.state=data.state.astype(int)
# data=data[['case:concept:name','concept:name','state','time:timestamp']]
# count= data.groupby(['state'])['concept:name'].count()
# count=count[count<5]
# count=count.reset_index()
# low_freq=count.state
#
# filtered_case=data[data.state.isin(list(low_freq))]
# filtered_case=filtered_case['case:concept:name']
#
# temp=data['case:concept:name'].isin(list(filtered_case))
# filtered_log=data[~temp]
#
# print(data['case:concept:name'].nunique())
# print(filtered_log['case:concept:name'].nunique())
#
# d1= DAFSA(["BDE", "CBDE", "BDE", "CBDF", "BDF"], delimiter='')
# # # d1= DAFSA(["B D E", "C B D E", "B D E", "C B D F", "B D F"], delimiter=' ')
# #
# # d2= DAFSA(["B;D;E", "C;B;D;E", "B;D;E", "C;B;D;F", "B;D;F"], delimiter=';')
# #
# # print(d2.lookup_nodes[0].edges['B'].node.node_id)
# #
# # #building a dataframe
# # traces=["B;D;E", "C;B;D;E", "B;D;E", "C;B;D;F", "B;D;F"]
# # result=[]
# # idx=0
# # for trace in traces:
# #     split= trace.split(';')
# #
# #     for i in split:
# #         res=[]
# #         res.append(idx)
# #         res.append(i)
# #         result.append(res)
# #
# #     idx+=1
# #
# # data=pd.DataFrame.from_records(result)
# # data.columns=['caseID','Activity']
# # # annotate event log from dafsa
# # states=[]
# # prev_state=0
# # curr_trace= -1
# # for idx, row in data.iterrows():
# #     if curr_trace != row['caseID']:
# #         prev_state = 0
# #         curr_trace = row['caseID']
# #
# #     else:
# #         prev_state = curr_state
# #
# #     curr_state = d2.lookup_nodes[prev_state].edges[row['Activity']].node.node_id
# #     states.append(curr_state)
# #
# # data['state']=states
# #
# #
# # print(d1)
# # print("************")
# # print(d2)
# #
# # # d=DAFSA()
# # # print(d.lookup("tapppp"))
# # # d.write_figure("example.png",working_dir=r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\amun")
# #
# # # g=d.to_graph()
# # # nx.draw(g, with_labels=True, font_weight='bold')
# # # # plt.show()
