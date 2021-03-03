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

def anonymize_event_log(data_dir=r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\data",
                        out_dir=r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\anonymized_logs",
                        dataset="BPIC13_t",
                        delta=0.5,
                        precision=0.5,
                        iteration=1):


    start_all = time.time()

    # delta=0.8
    # precision =0.5
    # temp directory name tmp/t_ event log name _ precision _ delta _ itertion
    curr_dir = os.getcwd()
    temp_dir=os.path.join(curr_dir, 'tmp','t_%s_%s_%s_%s'%(dataset,precision,delta,iteration))

    data, variants_count = event_log_anonymization(data_dir, dataset, delta, precision, temp_dir)

    end_all = time.time()
    print("wall-to-wall execution time is: %s  seconds"  %(end_all - start_all))



    # calculate the SMAPE
    data, smape_time, smape_variant=estimate_SMAPE_variant_and_time(data, variants_count)
    print("SMAPE time: %s %%"%(smape_time))
    print("SMAPE case variant: %s %%" % (smape_variant))
    # return from relative time to original timestamps
    data=relative_time_to_XES(data,dataset,out_dir)


if __name__ == "__main__":
    if not sys.warnoptions:
        warnings.simplefilter("ignore")

    datasets = ["CCC19_t", "Sepsis_t", "Unrineweginfectie_t", "BPIC14_t", "Traffic_t", "Hospital_t", "CreditReq_t", "BPIC20_t",
                "BPIC12_t", "BPIC13_t", "BPIC15_t", "BPIC17_t", "BPIC18_t", "BPIC19_t"]


    datasets = ['Sepsis_t']

    data_dir="data"
    out_dir="anonymized_logs"


    for dataset in datasets:
        anonymize_event_log(data_dir,out_dir,dataset)


