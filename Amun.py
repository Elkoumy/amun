"""
This module implements the main module for the event log anonymizer

"""

from amun.event_log_anonymization import event_log_anonymization
from amun.measure_accuracy import estimate_SMAPE_variant_and_time
from amun.log_exporter import relative_time_to_XES, relative_time_to_XES2, export_csv, adding_dummy_columns
import time
#import swifter
import sys
import warnings
import os
import pandas as pd
def anonymize_event_log(data_dir=r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\data",
                        out_dir=r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\anonymized_logs",
                        experiment_log_dir="",
                        dataset="BPIC13_t",
                        mode='sampling',
                        delta=0.5):


    start_all = time.time()


    curr_dir = os.path.dirname(os.path.realpath(__file__))
    temp_dir=os.path.join(curr_dir, 'tmp','t_%s%s_delta%s'%(dataset,mode,delta))

    data, variants_count = event_log_anonymization(data_dir, dataset, mode, delta,  temp_dir)



    #creating separate folder for each delta and for each precision
    if not os.path.isdir(os.path.join( out_dir)):
        # create the dir if it doesn't exist
        os.mkdir(os.path.join( out_dir))

    # if not os.path.isdir(os.path.join( out_dir,'delta_%s'%(delta))):
    #     # create the dir if it doesn't exist
    #     os.mkdir(os.path.join( out_dir,'delta_%s'%(delta)))
    #
    # if not os.path.isdir(os.path.join( out_dir,'delta_%s'%(delta),'precision_%s'%(precision))):
    #     # create the dir if it doesn't exist
    #     os.mkdir(os.path.join( out_dir,'delta_%s'%(delta),'precision_%s'%(precision)))
    #
    # out_dir=os.path.join( out_dir,'delta_%s'%(delta),'precision_%s'%(precision))



    file_name='e_anonymized_%s_%s_delta%s'%(dataset,mode,delta)
    # return from relative time to original timestamps
    data=relative_time_to_XES2(data,out_dir,file_name)
    # data=export_csv(data,out_dir,file_name)





if __name__ == "__main__":
    if not sys.warnoptions:
        warnings.simplefilter("ignore")


    # dataset = "Sepsis"
    # mode = 'sampling'
    # modes=['oversampling','filtering','sampling']
    # delta = 0.2

    dataset = os.sys.argv[1]
    mode = os.sys.argv[2]
    delta = float(os.sys.argv[3])

    # modes=['oversampling','filtering','sampling']
    cur_dir=os.path.dirname(os.path.realpath(__file__))
    data_dir=os.path.join(cur_dir,'input_logs')
    if not os.path.isdir(os.path.join( data_dir)):
        # create the dir if it doesn't exist
        os.mkdir(os.path.join( data_dir))


    out_dir=os.path.join(cur_dir,"output")
    if not os.path.isdir(os.path.join( out_dir)):
        # create the dir if it doesn't exist
        os.mkdir(os.path.join( out_dir))


    experiment_log_dir=os.path.join(cur_dir,'experiment_event_anonymizer_log')
    if not os.path.isdir(os.path.join( experiment_log_dir)):
        # create the dir if it doesn't exist
        os.mkdir(os.path.join( experiment_log_dir))


    anonymize_event_log(data_dir,out_dir,experiment_log_dir,dataset,mode,delta)


