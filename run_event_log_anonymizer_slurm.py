"""
This module implements the main module for the event log anonymizer

"""

from amun.event_log_anonymization import event_log_anonymization
from amun.measure_accuracy import estimate_SMAPE_variant_and_time
from amun.log_exporter import relative_time_to_XES
import time
#import swifter
import sys
import warnings
import os
import pandas as pd
from run_event_log_anonymizer import anonymize_event_log


if __name__ == "__main__":
    if not sys.warnoptions:
        warnings.simplefilter("ignore")

    datasets = ["CCC19_t", "Sepsis_t", "Unrineweginfectie_t", "BPIC14_t", "Traffic_t", "Hospital_t", "CreditReq_t", "BPIC20_t",
                "BPIC12_t", "BPIC13_t", "BPIC15_t", "BPIC17_t", "BPIC18_t", "BPIC19_t"]

    # make the dataset to come from the arguments

    cur_dir=os.path.dirname(os.path.realpath(__file__))
    data_dir=os.path.join(cur_dir,'data')
    out_dir=os.path.join(cur_dir,"anonymized_logs")
    experiment_log_dir=os.path.join(cur_dir,'experiment_event_anonymizer_log')

    dataset = os.sys.argv[1]
    mode=os.sys.argv[2]
    delta= float(os.sys.argv[3])
    precision=float(os.sys.argv[4])
    iteration=int(os.sys.argv[5])

    anonymize_event_log(data_dir, out_dir, experiment_log_dir, dataset,mode, delta, precision, iteration)



