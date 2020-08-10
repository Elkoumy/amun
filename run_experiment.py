"""
In this file, we run the experiments for different files

"""

from differental_privacy_module import *
# from GUI_module import *
from input_module import *


# DFG as a counter object
# dfg_freq, dfg_time = read_xes("sample_data/manufacurer.xes")

# dfg_freq, dfg_time = read_xes(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Data\Data XES\CCC19.xes")
# dfg_freq, dfg_time = read_xes(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Data\Data XES\Sepsis Cases - Event Log.xes")
dfg_freq, dfg_time = read_xes(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Data\Data XES\Road_Traffic_Fine_Management_Process.xes")


emd_freq_tot=0
emd_time_tot=0
for i in range(0,100):
    dfg_freq_new, dfg_time_new, epsilon_freq,epsilon_time, emd_freq, emd_time = differential_privacy_with_risk(dfg_freq, dfg_time, delta=0.05,precision=0.1)
    # print("EMD for frequency is "+ str(emd_freq))
    # print("EMD for time is "+ str(emd_time))
    emd_freq_tot+=emd_freq
    emd_time_tot+= emd_time

print("avg EMD for freq is " + str(emd_freq_tot/100))
print("avg EMD for time is " + str(emd_time_tot/100))


dfg_freq_new, dfg_time_new, epsilon_freq, epsilon_time, delta_freq , delta_time=differential_privacy_with_accuracy(dfg_freq, dfg_time,precision=0.1, distance=1000, aggregate_type=AggregateType.SUM)

print("delta for the freq is "+ str(delta_freq))
print("delta for the time is "+ str(delta_time))

