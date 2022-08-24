from amun.amun.event_log_anonymization import event_log_anonymization
from amun.amun.input_module import xes_to_DAFSA
from amun.amun.measure_accuracy import estimate_SMAPE_variant_and_time
from amun.amun.log_exporter import relative_time_to_XES,relative_time_to_XES2
import time
#import swifter
import sys
import warnings
import os
import pandas as pd
def get_stats(data_dir=r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\data",
                        dataset="BPIC13_t"
                       ):
    """
        For each of the logs we used in the BPM paper, I would like to know:
        - The number of states in the DAFSA of that log
        - The number of transitions in the DAFSA of that log
        - The number of events in that log (i.e. the total number of rows in the event log)
        """

    data, variants_count = xes_to_DAFSA(data_dir, dataset)
    states_count=data.state.unique().shape[0]+1 # + state 0
    transitions = data[['prev_state', 'concept:name', 'state']]
    transition_count=transitions.groupby(['prev_state','concept:name','state']).size().shape[0]
    event_count=data.shape[0]
    return [dataset,states_count, transition_count, event_count ]




if __name__ == "__main__":
    if not sys.warnoptions:
        warnings.simplefilter("ignore")

    datasets = ["CCC19_t", "Sepsis_t", "Unrineweginfectie_t", "BPIC14_t", "Traffic_t", "Hospital_t", "CreditReq_t", "BPIC20_t",
                "BPIC12_t", "BPIC13_t", "BPIC15_t", "BPIC17_t", "BPIC18_t", "BPIC19_t"]


    # datasets=["Sepsis_t"]


    # cur_dir=os.getcwd()
    cur_dir=os.path.dirname(os.path.realpath(__file__))
    data_dir=os.path.join(cur_dir,'data')

    result=[]
    for dataset in datasets:
            print("Current Dataset: %s"%(dataset))
            result.append(get_stats(data_dir,dataset))

    result=pd.DataFrame.from_records(result)
    result.columns=['event_log','states_count', 'transition_count', 'event_count' ]
    result.to_csv("DAFSA_stats.csv", index=False)
    print(result)