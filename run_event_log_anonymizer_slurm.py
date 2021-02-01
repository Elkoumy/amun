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
import gc
#import swifter
from statsmodels.distributions.empirical_distribution import ECDF
import sys
import warnings
import os

def anonymize_event_log(data_dir=r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\data",
                        dataset="BPIC13_t"):
    # data_dir=r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\data"
    # dataset="temp"
    # dataset="CCC19_t"
    # dataset="Sepsis_t"
    # dataset="CreditReq_t"
    # dataset="BPIC12_t"
    # dataset="BPIC19"
    # dataset="Unrineweginfectie_t"
    # dataset="Hospital_t"
    # dataset="Traffic_t"
    # dataset="Sepsis_t"
    #event logs without lifecycle.
    #"BPIC13", "BPIC20", "BPIC19", "BPIC14", "Unrineweginfectie", "temp"

    print("Processing the dataset: %s"%(dataset))
    start_all = time.time()

    start = time.time()
    data, trace_variants= xes_to_DAFSA(data_dir, dataset)
    # data, trace_variants= xes_to_prefix_tree(data_dir, dataset)
    end = time.time()
    print("reading to DAFSA annotation %s" %(end - start))



    delta=0.2
    precision =0.00000000001
    #TODO: calculate noise here
    noise=3

    #move epsilon estimation before the trace anonymization
    data=data[['case:concept:name','concept:name','time:timestamp','relative_time','trace_variant','prev_state','state']]
    start=time.time()
    #TODO: optimize epsilon estimation
    data=estimate_epsilon_risk_vectorized(data,delta, precision)
    end=time.time()
    print("estimate epsilon :  %s"%(end-start))




    start = time.time()
    data=anonymize_traces(data,noise)
    end = time.time()
    print("anonymize traces %s" %(end - start))

    end_all = time.time()
    print("wall-to-wall execution time is: %s  seconds"  %(end_all - start_all))

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


if __name__ == "__main__":
    if not sys.warnoptions:
        warnings.simplefilter("ignore")

    datasets = ["CCC19_t", "Sepsis_t", "Unrineweginfectie_t", "BPIC14_t", "Traffic_t", "Hospital_t", "CreditReq_t", "BPIC20_t",
                "BPIC12_t", "BPIC13_t", "BPIC15_t", "BPIC17_t", "BPIC18_t", "BPIC19_t"]

    # make the dataset to come from the arguments

    data_dir = os.sys.argv[1]
    dataset = os.sys.argv[2]
    anonymize_event_log(data_dir,dataset)


