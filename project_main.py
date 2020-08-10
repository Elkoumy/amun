'''
    Main project file
    The project performs the following functionalities:
    * Reading the event logs as XES or reading DFGs.
    * Take either delta as input or accuracy as input.
    * Report the epsilon, delta and accuracy.
    * Plot the DFG for both cases.
    * export the DFG after applying the differential privacy.
'''

from differental_privacy_module import *
# from GUI_module import *
from input_module import *


# DFG as a counter object
dfg_freq, dfg_time = read_xes("sample_data/manufacurer.xes")

# dfg_freq_new = Counter()

# for key in dfg_freq.keys():
#     dfg_freq_new[key] = dfg_freq[key]
#     break

# dfg_freq=dfg_freq_new

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


dfg_freq_new, dfg_time_new, epsilon_freq, epsilon_time, delta_freq , delta_time=differential_privacy_with_accuracy(dfg_freq, dfg_time,precision=0.1, distance=10, aggregate_type=AggregateType.SUM)

print("delta for the freq is "+ str(delta_freq))
print("delta for the time is "+ str(delta_time))

