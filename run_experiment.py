"""
In this file, we run the experiments for different files

"""

from differental_privacy_module import *
# from GUI_module import *
from input_module import *
import pandas as pd
import sys


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

data_dir =r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Data\Data XES"
# datasets=["CCC19","Sepsis Cases - Event Log","CoSeLoG_WABO_2","BPIC15_2","CreditRequirement","BPIC15_1","Hospital_log","Road_Traffic_Fine_Management_Process"]
datasets=["CCC19","Sepsis Cases - Event Log","CoSeLoG_WABO_2"]

result_log_delta = []  # holds the delta as input exeperiment
# vales is exp_index, delta, epsilon_freq, epsilon_time, emd_freq, emd_time

result_log_alpha=[] # holds the alpha or EMD as input exeperiment

for dataset in datasets:
    dfg_freq, dfg_time = read_xes(data_dir+"\\"+dataset+".xes")
    aggregate_types=[AggregateType.AVG, AggregateType.SUM]
    for aggregate_type in aggregate_types:
        # delta=0.05
        deltas=[0.01,0.05, 0.1, 0.5]
        for delta in deltas:
            precision=0.1
            no_of_experiments=10

            emd_freq_tot=0
            emd_time_tot=0

            for i in range(0,no_of_experiments):
                dfg_freq_new, dfg_time_new, epsilon_freq,epsilon_time, emd_freq, emd_time = differential_privacy_with_risk(dfg_freq, dfg_time, delta=delta,precision=precision,aggregate_type=aggregate_type)
                # print("EMD for frequency is "+ str(emd_freq))
                # print("EMD for time is "+ str(emd_time))
                emd_freq_tot+=emd_freq
                emd_time_tot+= emd_time

                #log the results
                # print(epsilon_time)
                # print(min(epsilon_time.values()))
                # result_log_delta.append([dataset,i,delta,epsilon_freq,min(epsilon_time.values()), emd_freq, emd_time]) # logging the min epsilon for time as it is the maximum added noise

            print("avg EMD for freq is " + str(emd_freq_tot/no_of_experiments))
            print("avg EMD for time is " + str(emd_time_tot/no_of_experiments))
            result_log_delta.append([dataset,aggregate_type, i, delta, epsilon_freq, min(epsilon_time.values()), emd_freq_tot/no_of_experiments,
                                     emd_time_tot/no_of_experiments])  # logging the min epsilon for time as it is the maximum added noise




        # emd=1000
        emds=[10,50,100,500,1000,5000,10000]
        for emd in emds:
            precision=0.1

            dfg_freq_new, dfg_time_new, epsilon_freq, epsilon_time, delta_freq , delta_time=differential_privacy_with_accuracy(dfg_freq, dfg_time,precision=precision, distance=emd, aggregate_type=aggregate_type)

            result_log_alpha.append([dataset,aggregate_type,0,emd,epsilon_freq, epsilon_time, delta_freq , delta_time])

            print("delta for the freq is "+ str(delta_freq))
            print("delta for the time is "+ str(delta_time))


        # transform results into dataframes
        result_log_delta=pd.DataFrame.from_records(result_log_delta,columns=["dataset","aggregate_type","exp_indx", "delta", "epsilon_freq", "epsilon_time", "emd_freq", "emd_time"])
        result_log_delta.to_csv("result_log_delta.csv",index=False)
        result_log_alpha=pd.DataFrame.from_records(result_log_alpha, columns =["dataset","aggregate_type","exp_indx", "alpha", "epsilon_freq", "epsilon_time", "delta_freq", "delta_time"])
        result_log_alpha.to_csv("result_log_alpha.csv",index=False)