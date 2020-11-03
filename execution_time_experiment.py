"""
In this file, we run the experiments for different files

"""

from amun.differental_privacy_module import *
# from GUI_module import *
from amun.input_module import *
import pandas as pd
from amun.data_visualization import plot_results
from statistics import median
from amun.model_visualization import view_model
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

        dfg_new, dfg_new, epsilon,  MAPE, SMAPE, APE_dist, SMAPE_dist = differential_privacy_with_risk(dfg, delta=delta,precision=precision,aggregate_type=aggregate_type)
        end_time = time.time()



    else:

        emd = float(input_alpha_delta)

        dfg_new, epsilon, delta , delta_dfg, delta_per_event = differential_privacy_with_accuracy(dfg, precision=precision,
                                                                                distance=emd,
                                                                                aggregate_type=aggregate_type)
        end_time = time.time()

    print("time = " + str(end_time - start_time))
    time_diff_alpha = end_time - start_time
    log = []
    log.append([dataset, parameter, mode, aggregate_type, input_val, time_diff_alpha])
    log = pd.DataFrame.from_records(log)
    log.to_csv(os.path.join(log_dir, "execution_time_%s_%s_%s_%s_%s.csv" % (
        input_dataset, str(input_alpha_delta), mode, aggregate_type, input_val)), index=False)


if __name__ == "__main__":
    init(4)
    data = os.sys.argv[1]
    parameter = os.sys.argv[2]
    mode = os.sys.argv[3]
    aggregate_type = os.sys.argv[4]
    input_val = os.sys.argv[5]

    if aggregate_type == "AggregateType.FREQ":
        aggregate_type = AggregateType.FREQ
    elif aggregate_type == "AggregateType.MIN":
        aggregate_type = AggregateType.MIN
    elif aggregate_type == "AggregateType.MAX":
        aggregate_type = AggregateType.MAX
    elif aggregate_type == "AggregateType.AVG":
        aggregate_type = AggregateType.AVG
    elif aggregate_type == "AggregateType.SUM":
        aggregate_type = AggregateType.SUM

    run_experiment(data=data, parameter=parameter, mode=mode, aggregate_type=aggregate_type, input_val=input_val)
