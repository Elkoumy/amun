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
# datasets=["CCC19","Sepsis Cases - Event Log","CoSeLoG_WABO_2","BPIC15_2","CreditRequirement","BPIC15_1","Hospital_log","Road_Traffic_Fine_Management_Process"]
datasets=["Sepsis Cases - Event Log","CoSeLoG_WABO_2","BPIC15_2"]
# datasets=["Sepsis Cases - Event Log","CoSeLoG_WABO_2"]

result_log_delta = []  # holds the delta as input exeperiment
# vales is exp_index, delta, epsilon_freq, epsilon_time, emd_freq, emd_time

result_log_alpha=[] # holds the alpha or EMD as input exeperiment
# delta_per_distance={}

delta_logger_time=[]
delta_logger_freq=[]


no_of_experiments=100
precision=0.1
for dataset in datasets:

    # aggregate_types=[AggregateType.AVG, AggregateType.SUM]
    aggregate_types = [ AggregateType.AVG, AggregateType.SUM,AggregateType.MIN,AggregateType.MAX]
    for aggregate_type in aggregate_types:
        print("Dataset: "+ dataset)
        print("Aggregate Type: "+ str(aggregate_type))
        # delta=0.05
        dfg_freq, dfg_time = read_xes(data_dir + "\\" + dataset + ".xes", aggregate_type)
        deltas=[0.01,0.05, 0.1,0.2,0.3,0.4,0.5,0.6, 0.7,0.8,0.9]
        for delta in deltas:


            emd_freq_tot=0
            emd_time_tot=0
            epsilon_time_min=0
            for i in range(0,no_of_experiments):
                dfg_freq_new, dfg_time_new, epsilon_freq,epsilon_time, emd_freq, emd_time, percent_freq,percent_time , percent_freq_dist,percent_time_dist = differential_privacy_with_risk(dfg_freq, dfg_time, delta=delta,precision=precision,aggregate_type=aggregate_type)
                # print("EMD for frequency is "+ str(emd_freq))
                # print("EMD for time is "+ str(emd_time))
                # emd_freq_tot+=emd_freq
                # emd_time_tot+= emd_time
                # emd_freq_tot+=percent_freq
                # emd_time_tot+= percent_time

                emd_freq_tot+=median(percent_freq_dist.values())
                emd_time_tot+=median(percent_time_dist.values())
                epsilon_time_min+=min(epsilon_time.values())
                #log the results
                # print(epsilon_time)
                # print(min(epsilon_time.values()))
                # result_log_delta.append([dataset,i,delta,epsilon_freq,min(epsilon_time.values()), emd_freq, emd_time]) # logging the min epsilon for time as it is the maximum added noise
                view_model(dfg_freq_new,process_model_dir+r"/fig_input_delta_"+str(delta)+"_"+dataset+"_"+str(aggregate_type)+"_"+str(i))
            print("avg median EMD for freq is " + str(emd_freq_tot/no_of_experiments))
            print("avg median EMD for time is " + str(emd_time_tot/no_of_experiments))
            result_log_delta.append([dataset,aggregate_type,  delta, epsilon_freq, epsilon_time_min/no_of_experiments, emd_freq_tot/no_of_experiments,
                                     emd_time_tot/no_of_experiments])  # logging the min epsilon for time as it is the maximum added noise




        # emd=1000
        emds=[0.01, 0.05, 0.1,0.2,0.3,0.4,0.5,0.6, 0.7,0.8,0.9]
        for emd in emds:


            dfg_freq_new, dfg_time_new, epsilon_freq, epsilon_time, delta_freq , delta_time, delta_freq_dfg, delta_time_dfg=differential_privacy_with_accuracy(dfg_freq, dfg_time,precision=precision, distance=emd, aggregate_type=aggregate_type)
            # delta_per_distance[emd] = delta_time_dfg
            for edge in delta_time_dfg.keys():
                delta_logger_time.append([dataset, aggregate_type, emd,delta_time_dfg[edge]])

            for edge in delta_freq_dfg.keys():
                delta_logger_freq.append([dataset, aggregate_type, emd,delta_freq_dfg[edge]])
            result_log_alpha.append([dataset,aggregate_type,emd,min(list(epsilon_freq.values())), min(list(epsilon_time.values())) , median(list(delta_freq_dfg.values())), median(list(delta_time_dfg.values())) , max(list(delta_freq_dfg.values())), max(list(delta_time_dfg.values())) ])
            view_model(dfg_freq_new, process_model_dir + r"/fig_input_emd_" + str(emd) + "_" + dataset + "_" + str(aggregate_type))
            print("delta for the freq is "+ str(delta_freq))
            print("delta for the time is "+ str(delta_time))




# transform results into dataframes
result_log_delta=pd.DataFrame.from_records(result_log_delta,columns=["dataset","aggregate_type", "delta", "epsilon_freq", "epsilon_time", "emd_freq", "emd_time"])
result_log_delta.to_csv(r"experiment_logs/result_log_delta.csv",index=False)
result_log_alpha=pd.DataFrame.from_records(result_log_alpha, columns =["dataset","aggregate_type", "alpha", "epsilon_freq", "epsilon_time", "delta_freq_median", "delta_time_median", "delta_freq_max", "delta_time_max"])
result_log_alpha.to_csv(r"experiment_logs/result_log_alpha.csv",index=False)

# #the delta distribution from emd as input
delta_logger_time=pd.DataFrame(delta_logger_time, columns=["dataset","aggregate_type","emd","delta"])
delta_logger_time.to_csv(r"experiment_logs/delta_logger_time.csv", index=False)

delta_logger_freq=pd.DataFrame(delta_logger_freq, columns=["dataset","aggregate_type","emd","delta"])
delta_logger_freq.to_csv(r"experiment_logs/delta_logger_freq.csv", index=False)
# plot_delta_distribution_times(delta_logger_time)

#plot the results
plot_results(result_log_delta,result_log_alpha,delta_logger_freq,delta_logger_time)
