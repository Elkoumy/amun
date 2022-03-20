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
                        delta=0.5,
                        ):


    start_all = time.time()

    # delta=0.8
    precision =0.0
    iteration=0
    # temp directory name tmp/t_ event log name _ precision _ delta _ itertion
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    temp_dir=os.path.join(curr_dir, 'tmp','t_%s%s_%s'%(dataset,mode,delta))

    data, variants_count = event_log_anonymization(data_dir, dataset, mode, delta,  temp_dir)

    end_all = time.time()
    print("wall-to-wall execution time is: %s  seconds"  %(end_all - start_all))

    # preparing the output logging

    result = [[dataset, precision, delta, iteration, (end_all - start_all)]]
    result = pd.DataFrame(result)
    result.to_csv(os.path.join(experiment_log_dir, 'wall_to_wall_execution_time',
                               'time_%s_%s_%s.csv' % (dataset,mode, delta)),
                  index=False,
                  header=False
                  )



    # calculate the SMAPE

    data, smape_time, smape_variant,oversampling_ratio,oversampling_df=estimate_SMAPE_variant_and_time(data, variants_count)
    print("SMAPE time: %s %%"%(smape_time))
    print("SMAPE case variant: %s %%" % (smape_variant))

    #preparing the output logging
    # log median epsilon
    result=[[dataset,precision,delta,iteration,smape_time,smape_variant,oversampling_ratio,data.eps.median(),data.eps_trace.loc[0]]]
    result=pd.DataFrame(result)
    result.to_csv(os.path.join(experiment_log_dir,'error_metrics','error_metric_%s_%s_%s_%s_%s.csv'%(dataset,mode,precision,delta,iteration)),
                  index=False,
                  header=False
                  )

    oversampling_df.to_csv(os.path.join(experiment_log_dir,'error_metrics','oversampling_per_variant_%s_%s_%s_%s_%s.csv'%(dataset,mode,precision,delta,iteration)),
                  index=False,
                  header=False
                  )

    #creating separate folder for each delta and for each precision
    if not os.path.isdir(os.path.join( out_dir)):
        # create the dir if it doesn't exist
        os.mkdir(os.path.join( out_dir))

    if not os.path.isdir(os.path.join( out_dir,'delta_%s'%(delta))):
        # create the dir if it doesn't exist
        os.mkdir(os.path.join( out_dir,'delta_%s'%(delta)))

    if not os.path.isdir(os.path.join( out_dir,'delta_%s'%(delta),'precision_%s'%(precision))):
        # create the dir if it doesn't exist
        os.mkdir(os.path.join( out_dir,'delta_%s'%(delta),'precision_%s'%(precision)))

    out_dir=os.path.join( out_dir,'delta_%s'%(delta),'precision_%s'%(precision))

    epsilons = {'dataset':['%s_p%s_d%s_i%s'%(dataset,precision,delta,iteration)],'event_eps_min': [data.eps.min()], 'event_eps_median': [data.eps.median()],
                'event_eps_mean': [data.eps.mean()], 'event_eps_max': [data.eps.max()], 'trace_eps': [data.eps_trace[0]]}
    epsilons = pd.DataFrame.from_dict(epsilons, orient='columns')
    eps_filename=os.path.join(experiment_log_dir,'epsilons','epsilon_%s_%s_p%s_d%s_i%s.csv'%(dataset,mode,precision,delta,iteration))
    epsilons.to_csv(eps_filename,index=False)

    file_name='e_anonymized_%s_%s_p%s_d%s_i%s'%(dataset,mode,precision,delta,iteration)
    # return from relative time to original timestamps
    data=relative_time_to_XES2(data,out_dir,file_name)
    # data=export_csv(data,out_dir,file_name)


    slurm_end_all = time.time()
    print("slurm wall-to-wall execution time is: %s  seconds" % (slurm_end_all - start_all))

    # preparing the output logging
    result = [[dataset, precision, delta, iteration, (slurm_end_all - start_all)]]
    result = pd.DataFrame(result)
    result.to_csv(os.path.join(experiment_log_dir, 'slurm_time',
                               'slurm_time_%s_%s_%s_%s_%s.csv' % (dataset,mode, precision, delta, iteration)),
                  index=False,
                  header=False

                  )


if __name__ == "__main__":
    if not sys.warnoptions:
        warnings.simplefilter("ignore")

    # datasets = ["CCC19_t", "Sepsis_t", "Unrineweginfectie_t", "BPIC14_t", "Traffic_t", "Hospital_t", "CreditReq_t", "BPIC20_t",
    #             "BPIC12_t", "BPIC13_t", "BPIC15_t", "BPIC17_t", "BPIC18_t", "BPIC19_t"]



    # deltas=[0.1,0.2,0.3,0.4,0.5]
    # precisions=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

    precisions=[0.2]
    deltas=[0.2,0.3,0.4]
    deltas = [0.2]
    deltas = [0.01, 0.075, 0.4]

    # datasets = ["CCC19_t",  "Unrineweginfectie_t", "Sepsis_t","Traffic_t", "Hospital_t", "CreditReq_t", "BPIC15_t","BPIC20_t", "BPIC13_t",
    # "BPIC12_t", "BPIC17_t", "BPIC14_t", "BPIC19_t" ]
    # datasets = ["CCC19_t", "Unrineweginfectie_t",  "Traffic_t", "Hospital_t", "CreditReq_t", "BPIC15_t",
    #             "BPIC20_t", "BPIC13_t", "BPIC17_t", "BPIC14_t", "BPIC19_t" ]

    datasets=[ "BPIC17_t" ]

    # modes=['oversampling','filtering','sampling']
    modes=['oversampling']
    # cur_dir=os.getcwd()
    cur_dir=os.path.dirname(os.path.realpath(__file__))
    data_dir=os.path.join(cur_dir,'data')
    out_dir=os.path.join(cur_dir,"anonymized_logs")
    experiment_log_dir=os.path.join(cur_dir,'experiment_event_anonymizer_log')

    # no_of_iterations=10
    no_of_iterations = 1

    for precision in precisions:

        for delta in deltas:

            for dataset in datasets:
                for mode in modes:
                    for iteration in range(0,no_of_iterations):
                        anonymize_event_log(data_dir,out_dir,experiment_log_dir,dataset,mode,delta)


