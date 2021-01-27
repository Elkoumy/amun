"""
This module implements the main module for the event log anonymizer

"""

import pandas as pd
import numpy as np
from pm4py.objects.conversion.log import factory as conversion_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter
from amun.input_module import xes_to_DAFSA, xes_to_prefix_tree
from amun.guessing_advantage import  estimate_epsilon_risk_dataframe, calculate_cdf_dataframe,estimate_epsilon_risk_dataframe2,estimate_epsilon_risk_vectorized
from amun.trace_anonymization import  anonymize_traces
import time
import swifter
from statsmodels.distributions.empirical_distribution import ECDF
#
data_dir=r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\data"
dataset="temp"
# dataset="CCC19"
dataset="Sepsis"
# dataset="CreditReq"
# dataset="BPIC12"
# dataset="BPIC19"
# dataset="Unrineweginfectie"
# dataset="Hospital"
# dataset="Traffic"

print("Running .....")
start = time.time()
data, trace_variants= xes_to_DAFSA(data_dir, dataset)
# data, trace_variants= xes_to_prefix_tree(data_dir, dataset)
end = time.time()
print("reading to DAFSA annotation %s" %(end - start))

delta=0.2
precision =0.00000000001
#TODO: calculate noise here
noise=3
start = time.time()
#move epsilon estimation before the trace anonymization
data=estimate_epsilon_risk_vectorized(data,delta, precision)
end = time.time()
print("epsilon estimation %s" %(end - start))




start = time.time()
# data=anonymize_traces(data,noise)
end = time.time()
print("anonymize traces %s" %(end - start))

#TODO: fix export error

# log = conversion_factory.apply(data[['case:concept:name','time:timestamp','concept:name']])
# #
# xes_exporter.export_log(log, dataset+"_anonymized.xes")

# start = time.time()


# data_cdf = data.groupby('state').relative_time.apply(calculate_cdf_dataframe)
# end = time.time()
# print("calculate cdf dataframe : %s" %(end - start))
#
# data_cdf['state']=data_cdf.index
#







