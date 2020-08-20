'''
    Main project file
    The project performs the following functionalities:
    * Reading the event logs as XES or reading DFGs.
    * Take either delta as input or accuracy as input.
    * Report the epsilon, delta and accuracy.
    * Plot the DFG for both cases.
    * export the DFG after applying the differential privacy.
'''

from amun.differental_privacy_module import *
# from GUI_module import *
from amun.input_module import *
from amun.data_visualization import plot_delta_distribution_time,plot_delta_distribution_freq
from amun.measure_accuracy import f1_score

aggregate_type=AggregateType.SUM

# DFG as a counter object
# dfg_freq, dfg_time = read_xes("sample_data/manufacurer.xes")
dfg_freq, dfg_time = read_xes(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Data\Data XES\Sepsis Cases - Event Log.xes", aggregate_type)

emd_freq_tot=0                                                                                                    
emd_time_tot=0

percentage_freq_tot=0
percentage_time_tot=0
no_of_experiments=5
delta=0.2
precision=0.5
for i in range(0,no_of_experiments):
    dfg_freq_new, dfg_time_new, epsilon_freq,epsilon_time, emd_freq, emd_time, percent_freq,percent_time = differential_privacy_with_risk(dfg_freq, dfg_time, delta=delta,precision=precision)
    # print("EMD for frequency is "+ str(emd_freq))
    # print("EMD for time is "+ str(emd_time))
    emd_freq_tot+=emd_freq
    emd_time_tot+= emd_time

    print("% time :"+str(percent_time))
    percentage_freq_tot+=percent_freq
    percentage_time_tot+=percent_time

    # res1,res2= f1_score(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Data\Data XES\Sepsis Cases - Event Log.xes", dfg_freq, dfg_freq_new)
    #
    # print("fitness 1: " + str(res1))
    # print("fitness 2: " + str(res2))



print("avg EMD for freq is " + str(emd_freq_tot/no_of_experiments))
print("avg EMD for time is " + str(emd_time_tot/no_of_experiments))


print("avg % for freq is " + str(percentage_freq_tot/no_of_experiments))
print("avg % for time is " + str(percentage_time_tot/no_of_experiments))

delta_per_distance_time={}
delta_per_distance_freq={}

distance= 0.1 # means %
dfg_freq_new, dfg_time_new, epsilon_freq, epsilon_time, delta_freq , delta_time, delta_freq_dfg, delta_time_dfg=differential_privacy_with_accuracy(dfg_freq, dfg_time,precision=precision, distance=distance, aggregate_type=aggregate_type)
delta_per_distance_time[distance]=delta_time_dfg
delta_per_distance_freq[distance]=delta_freq_dfg


plot_delta_distribution_time(delta_per_distance_time)
plot_delta_distribution_freq(delta_per_distance_freq)

print("delta for the freq is "+ str(delta_freq))
print("delta for the time is "+ str(delta_time))

