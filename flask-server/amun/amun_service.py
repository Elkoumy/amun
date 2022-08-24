"""
This module implements the main module for the event log anonymizer

"""
from pm4py.objects.conversion.log import factory as conversion_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter
# from amun.event_log_anonymization import event_log_anonymization


from amun.log_exporter import relative_time_to_timestamp

from amun.event_log_anonymization import event_log_anonymization


# from amun.log_exporter import relative_time_to_XES, relative_time_to_XES2, export_csv, adding_dummy_columns, relative_time_to_timestamp
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
    temp_dir=os.path.join(curr_dir, 'tmp', 't_%s%s_delta%s' % (dataset, mode, delta))

    data, variants_count,risk_per_event = event_log_anonymization(data_dir, dataset, mode, delta,  temp_dir)



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

    return data, risk_per_event







def amun(dataset, mode,delta):
    cur_dir = os.path.dirname(os.path.realpath(__file__))

    out_dir = os.path.join(cur_dir, "anonymized_logs")
    experiment_log_dir = os.path.join(cur_dir, 'experiment_event_anonymizer_log')


    #split dataset directory into dataset &data_dir
    data_dir = os.path.dirname(dataset)
    dataset=os.path.basename(dataset)

    data,risk_per_event=anonymize_event_log(data_dir, out_dir, experiment_log_dir, dataset, mode, delta)
    data = relative_time_to_timestamp(data)
    data=data[['case:concept:name', 'concept:name', 'time:timestamp', 'lifecycle:transition']]
    risk_per_event.columns=['case:concept:name', 'concept:name', 'time:timestamp', 'original_risk']

    # if input_type=='csv':
    #     data.to_csv(dataset)
    # else:
    #     log = conversion_factory.apply(data)
    #     xes_exporter.export_log(log, os.path.join(out_dir, dataset + ".xes"))

    # file_name='e_anonymized_%s_%s_delta%s'%(dataset,mode,delta)
    # # return from relative time to original timestamps
    # data=relative_time_to_XES2(data,out_dir,file_name)
    # # data=export_csv(data,out_dir,file_name)

    #return the anonymized log, risk per case, risk per edge
    return data,risk_per_event

#
# if __name__ == "__main__":
#     if not sys.warnoptions:
#         warnings.simplefilter("ignore")
#
#
#     dataset = r"C:\Users\elkoumy\OneDrive - Tartu Ülikool\Differential Privacy\flask-react-app\uploads\paper_example.csv"
#
#     mode = 'filtering'
#     # modes=['oversampling','filtering','sampling']
#     delta = 0.2
#
#     data,risk_pert_event =amun(dataset,mode,delta)



