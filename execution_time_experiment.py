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
# DFG as a counter object
# dfg_freq, dfg_time = read_xes("sample_data/manufacurer.xes")

# dfg_freq, dfg_time = read_xes(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Data\Data XES\CCC19.xes")
# dfg_freq, dfg_time = read_xes(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Data\Data XES\Sepsis Cases - Event Log.xes")
# dfg_freq, dfg_time = read_xes(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Data\Data XES\CoSeLoG_WABO_2.xes")
# dfg_freq, dfg_time = read_xes(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Data\Data XES\BPIC15_2.xes")
# dfg_freq, dfg_time = read_xes(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Data\Data XES\CreditRequirement.xes") #strange behavior with time delta
# dfg_freq, dfg_time = read_xes(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Data\Data XES\BPIC15_1.xes")
# dfg_freq, dfg_time = read_xes(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Data\Data XES\Hospital_log.xes")
# dfg_freq, dfg_time = read_xes(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Data\Data XES\Road_Traffic_Fine_Management_Process.xes")

# print(len(dfg_freq))
# sys.exit()

process_model_dir=r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\source code\experiment_figures\process_models"
data_dir =r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Data\Data XES"
figures_dir=r'C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\source code\experiment_figures'


# datasets=["Sepsis Cases - Event Log","CreditRequirement","Road_Traffic_Fine_Management_Process"]

datasets=["Road_Traffic_Fine_Management_Process"]



no_of_experiments=1
precision=0.5
for dataset in datasets:
    aggregate_type = AggregateType.MIN

    dfg_freq, dfg_time = read_xes(data_dir + "\\" + dataset + ".xes", aggregate_type)

    delta=0.1
    dfg_freq_new, dfg_time_new, epsilon_freq, epsilon_time, MAPE_freq, SMAPE_freq, APE_dist_freq, MAPE_time, SMAPE_time, APE_dist_time = differential_privacy_with_risk(
        dfg_freq, dfg_time, delta=delta, precision=precision, aggregate_type=aggregate_type)
    emd=0.1
    dfg_freq_new, dfg_time_new, epsilon_freq, epsilon_time, delta_freq, delta_time, delta_freq_dfg, delta_time_dfg = differential_privacy_with_accuracy(
        dfg_freq, dfg_time, precision=precision, distance=emd, aggregate_type=aggregate_type)


