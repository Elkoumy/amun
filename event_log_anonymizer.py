"""
This module implements the main module for the event log anonymizer

"""

import pandas as pd
import numpy as np

from amun.input_module import xes_to_DAFSA
from amun.guessing_advantage import  estimate_epsilon_risk_dataframe, calculate_cdf_dataframe
from amun.trace_anonymization import  anonymize_traces
import time
from statsmodels.distributions.empirical_distribution import ECDF
#
data_dir=r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\data"
# dataset="temp"
# dataset="CCC19"
# dataset="Sepsis"
# dataset="CreditReq"
# dataset="BPIC13"
dataset="Unrineweginfectie"

print("Running .....")
start = time.time()
data, trace_variants= xes_to_DAFSA(data_dir, dataset)
end = time.time()
print("reading to DAFSA annotation %s" %(end - start))

delta=0.2
precision =0.00000000001
#TODO: calculate noise here
noise=3

start = time.time()


data=anonymize_traces(data,noise)
end = time.time()
print("anonymize traces %s" %(end - start))


start = time.time()
data, trace_variants= xes_to_DAFSA(data_dir, dataset)

data_cdf = data.groupby('state').relative_time.apply(calculate_cdf_dataframe)
end = time.time()
print("calculate cdf dataframe : %s" %(end - start))

data_cdf['state']=data_cdf.index

data_state_max=data.groupby('state').relative_time.max()
data_state_max['state']=data_state_max.index

data= pd.merge(data, data_cdf, on=['state'], suffixes=("","_ecdf"))

data= pd.merge(data, data_state_max, on=['state'], suffixes=("","_max"))

start = time.time()
data['eps']=data.apply(lambda x: estimate_epsilon_risk_dataframe(x['relative_time'],x['relative_time_ecdf'],x['relative_time_max'], delta, precision), axis=1)
end = time.time()
print("epsilon estimation %s" %(end - start))

