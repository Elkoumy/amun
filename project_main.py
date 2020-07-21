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
from measure_accuracy import *
from visualizing_dfg import *

# DFG as a counter object
dfg_freq, dfg_time = read_xes("sample_data/manufacurer.xes")
dfg_freq, dfg_time, epsilon_freq,epsilon_time, accuracy = differential_privacy_with_risk(dfg_freq, dfg_time, delta=0.1,precision=0.1)
print( earth_mover_dist(dfg_freq,dfg_freq))

