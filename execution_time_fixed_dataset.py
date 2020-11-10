"""
In this file, we run the experiments for different files

"""

from amun.differental_privacy_module import *
# from GUI_module import *
from amun.input_module import *
import pandas as pd
# from amun.data_visualization import plot_results
from statistics import median
# from amun.model_visualization import view_model
import os
import time

from amun.multiprocessing_helper_functions import init


def run_experiment(data="Sepsis", parameter="0.1", mode="nonpruning", aggregate_type=AggregateType.AVG,
                   input_val="delta"):
    """Parameters to the script"""
    start_time = time.time()
    input_dataset = data
    input_alpha_delta = float(parameter)
    '''**********************'''
    dir_path = os.path.dirname(os.path.realpath(__file__))
    process_model_dir = os.path.join(dir_path, "experiment_figures", "process_models")
    data_dir = os.path.join(dir_path, "data")
    figures_dir = os.path.join(dir_path, 'experiment_figures')
    log_dir = os.path.join(dir_path, 'experiment_logs')

    precision = 0.5
    dataset = input_dataset

    print("Dataset: " + dataset)
    print("Aggregate Type: " + str(aggregate_type))
    dfg = read_xes(data_dir, dataset, aggregate_type, mode)

    if input_val == "delta":
        delta = float(input_alpha_delta)
        print("before differential privacy")
        dfg_new, dfg_new, epsilon,  MAPE, SMAPE, APE_dist, SMAPE_dist = differential_privacy_with_risk(dfg, delta=delta,precision=precision,aggregate_type=aggregate_type)
        print("after differential privacy")
        end_time = time.time()



    else:

        emd = float(input_alpha_delta)
        print("before differential privacy")
        dfg_new, epsilon, delta , delta_dfg, delta_per_event = differential_privacy_with_accuracy(dfg, precision=precision,
                                                                                distance=emd,
                                                                                aggregate_type=aggregate_type)
        print("before differential privacy")
        end_time = time.time()

    print("time = " + str(end_time - start_time))
    time_diff_alpha = end_time - start_time
    log = []
    log.append([dataset, parameter, mode, aggregate_type, input_val, time_diff_alpha])
    log = pd.DataFrame.from_records(log)
    log.to_csv(os.path.join(log_dir, "execution_time_%s_%s_%s_%s_%s.csv" % (
        input_dataset, str(input_alpha_delta), mode, aggregate_type, input_val)), index=False)


if __name__ == "__main__":
    # number of tasks
    datasets=["CCC19","Sepsis","Unrineweginfectie", "BPIC14","Traffic","Hospital","CreditReq","BPIC20","BPIC12","BPIC13","BPIC15","BPIC17","BPIC18","BPIC19"]
    datasets = ["CCC19", "Sepsis", "Unrineweginfectie", "BPIC14", "Traffic", "Hospital", "CreditReq", "BPIC20",
                "BPIC12", "BPIC13", "BPIC15", "BPIC17", "BPIC18", "BPIC19"]

    datasets=['BPIC14']
    # data='CCC19'
    # datasets = 'CreditReq'
    # parameters = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    parameters = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    # aggregate_types = [AggregateType.FREQ, AggregateType.AVG, AggregateType.SUM, AggregateType.MIN, AggregateType.MAX]
    aggregate_types = [AggregateType.SUM]
    input_values = ["delta", "alpha"]
    input_values = ["alpha"]
    mode = "nonpruning"
    for data in datasets:
        for input_val in input_values:
            if input_val == "delta":
                # for iteration in range(0,10):
                for iteration in range(0, 1):
                    for aggregate_type in aggregate_types:
                        for parameter in parameters:

                            run_experiment(data=data, parameter=parameter, mode=mode, aggregate_type=aggregate_type,
                                           input_val=input_val)

            else:
                for aggregate_type in aggregate_types:
                    for parameter in parameters:

                        run_experiment(data=data, parameter=parameter, mode=mode, aggregate_type=aggregate_type,
                                       input_val=input_val)
