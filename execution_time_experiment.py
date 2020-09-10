"""
In this file, we run the experiments for different files

"""

from amun.differental_privacy_module import *
from amun.input_module import *
import pandas as pd
from amun.data_visualization import plot_results
from statistics import median
import time
import seaborn as sns
import matplotlib.pyplot as plt
import os
process_model_dir=r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\source code\experiment_figures\process_models"
data_dir =r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Data\Data XES"
figures_dir=r'C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\source code\experiment_figures'


# datasets=["Sepsis Cases - Event Log","CreditRequirement","Road_Traffic_Fine_Management_Process"]

datasets=["Sepsis Cases - Event Log","CreditRequirement"]



no_of_experiments=1
precision=0.5
log=[]
for dataset in datasets:
    aggregate_type = AggregateType.MIN
    print("starting loading data")
    dfg_freq, dfg_time = read_xes(data_dir + "\\" + dataset + ".xes", aggregate_type)
    print("finish loading data")
    delta=0.1
    start_time = time.time()
    dfg_freq_new, dfg_time_new, epsilon_freq, epsilon_time, MAPE_freq, SMAPE_freq, APE_dist_freq, MAPE_time, SMAPE_time, APE_dist_time = differential_privacy_with_risk(
        dfg_freq, dfg_time, delta=delta, precision=precision, aggregate_type=aggregate_type)
    end_time = time.time()
    time_diff_delta=end_time-start_time
    print("delta time = "+str(end_time-start_time))
    log.append([dataset, aggregate_type, "delta", time_diff_delta])

    emd=0.1
    start_time = time.time()
    dfg_freq_new, dfg_time_new, epsilon_freq, epsilon_time, delta_freq, delta_time, delta_freq_dfg, delta_time_dfg = differential_privacy_with_accuracy(
        dfg_freq, dfg_time, precision=precision, distance=emd, aggregate_type=aggregate_type)
    end_time = time.time()

    print("alpha time = "+str(end_time-start_time))

    time_diff_alpha = end_time - start_time

    log.append([dataset, aggregate_type,"alpha",time_diff_alpha])

log.append(["Road_Traffic_Fine_Management_Process", aggregate_type,"delta",3189.7172985076904])
log.append(["Road_Traffic_Fine_Management_Process", aggregate_type,"alpha",4094.1853733062744])


log=pd.DataFrame.from_records(log,columns=["dataset","aggregate_type", "parameter", "time_diff"])
log.to_csv(r"experiment_logs/execution_time_log.csv", index=False)

# log=pd.read_csv(r"experiment_logs/execution_time_log.csv")

log['dataset'].replace('Road_Traffic_Fine_Management_Process','Traffic Fines',inplace=True)
log['dataset'].replace('Sepsis Cases - Event Log','Sepsis Cases',inplace=True)
log['dataset'].replace('CreditRequirement','Credit Requirement',inplace=True)

log['parameter'].replace('delta','Input Delta',inplace=True)
log['parameter'].replace('alpha','Input Alpha',inplace=True)


g=sns.lineplot("dataset", "time_diff","parameter", data=log)
g.set_ylabel("Execution Time Log(Seconds)")  # epsilon
g.set_xlabel("Dataset")  # delta

g.set( yscale="log")
plt.legend()
plt.savefig(os.path.join(figures_dir, 'execution_time.pdf'))
plt.show()

""" Execution time for the Road_Traffic_Fine_Management_Process"""
# alpha time = 4094.1853733062744

# delta time = 3189.7172985076904