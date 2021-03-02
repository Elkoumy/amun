"""
This module implements the main module for the event log anonymizer

"""

import pandas as pd
import numpy as np
from pm4py.objects.conversion.log import factory as conversion_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter
from amun.input_module import xes_to_DAFSA, xes_to_prefix_tree
from amun.guessing_advantage import  estimate_epsilon_risk_dataframe, calculate_cdf_dataframe,estimate_epsilon_risk_dataframe2,estimate_epsilon_risk_vectorized
from amun.guessing_advantage import estimate_epsilon_risk_vectorized_with_normalization
from amun.trace_anonymization import  anonymize_traces_compacted, anonymize_traces
from amun.noise_injection import laplace_noise_injection
from amun.measure_accuracy import relative_time_MAPE
from amun.log_exporter import relative_time_to_XES
import time
import gc
#import swifter
from statsmodels.distributions.empirical_distribution import ECDF
import sys
import warnings
import os
import shutil

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

    """ Clearing tmp folder"""
    curr_dir = os.getcwd()
    if os.path.isdir(os.path.join(curr_dir, 'tmp')):
        #delete tmp
        # os.remove(os.path.join(curr_dir, 'tmp'))
        shutil.rmtree(os.path.join(curr_dir, 'tmp'))

    #create tmp
    os.mkdir(os.path.join(curr_dir, 'tmp'))

    delta=0.2
    precision =0.5


    #move epsilon estimation before the trace anonymization
    data=data[['case:concept:name','concept:name','time:timestamp','relative_time','trace_variant','prev_state','state']]
    start=time.time()
    #optimize epsilon estimation (memory issues)
    #TODO: Fix tmp directory for concurrent runs
    data=estimate_epsilon_risk_vectorized_with_normalization(data,delta, precision)
    print(data.relative_time_original)
    end=time.time()
    print("estimate epsilon :  %s"%(end-start))



    del(trace_variants)

    gc.collect()
    # TODO: calculate frequency noise here
    noise = 3

    start = time.time()
    # data=anonymize_traces(data,noise)

    data = anonymize_traces_compacted(data, noise)
    end = time.time()
    print("anonymize traces %s" %(end - start))


    #Laplace Noise Injection
    data= laplace_noise_injection(data)

    end_all = time.time()
    print("wall-to-wall execution time is: %s  seconds"  %(end_all - start_all))

    #TODO: calculate the accuracy here
    data,mape=relative_time_MAPE(data)

    #TODO: return from relative time to original timestamps
    out_dir=""
    relative_time_to_XES(data,out_dir)
    # log = conversion_factory.apply(data[['case:concept:name','concept:name','time:timestamp']])
    # xes_exporter.export_log(log, os.path.join(data_dir,dataset+"_anonymized.xes"))

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


    datasets = ['temp']
    data_dir="data"

    for dataset in datasets:
        anonymize_event_log(data_dir,dataset)


