# Amun
Amun is a framework that leverage recently developed Privacy-Enhancing Technologies (PETs) to help 
organizations publish anonymized process models. 
Amun uses a mathematically proven privacy model to 
balance the risk correlated with publishing process models and the utility after anonymization.
It uses an ε-differential-privacy mechanism to anonymize Directly-Follows Graphs (DFGs).
It provides a mathematical approach to calculate the value of ε that represents the amount of noise 
injected a process mining model that optimizes the risk and utility measures. 
Amun keeps all the traces and all the activities of a DFG. 
An emperical evaluation of Amun using 13 real-world event logs could be found our recent [paper](addlinkhere).
### Prerequisite

Installation of pm4py library for the support of XES files.
```
pip install pm4py
```

Install the differential privacy library
```
pip install diffprivlib
```

Install the multiprocessing library
```
pip install itertools
pip install multiprocessing
```

Install the statistics library
```
pip install statistics
```

### Usage
An example of the usage of Amun can be found in the file ```run_example.py```.
To perform the execution time experiment, you can use the file ```run_example_execution_time.py```. 
An implementation of Amun with a single thread could be found in the branch ```amun-model```.


### Cite the Project
```
Add citation here.
```