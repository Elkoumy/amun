# Amun
Amun is a framework that leverage recently developed Privacy-Enhancing Technologies (PETs) to help 
organizations publish anonymized process models. 
Amun uses a mathematically proven privacy model to 
balance the risk correlated with publishing process models and the utility after anonymization.
It uses an ε-differential-privacy mechanism to anonymize Directly-Follows Graphs (DFGs).
It provides a mathematical approach to calculate the value of ε that represents the amount of noise 
injected a process mining model that optimizes the risk and utility measures. 
Amun keeps all the traces and all the activities of a DFG. 
An emperical evaluation of Amun using 13 real-world event logs could be found in our recent [paper](https://arxiv.org/pdf/2012.01119.pdf).

### Cite the Project
```
Elkoumy, Gamal, Alisa Pankova, and Marlon Dumas. "Privacy-Preserving Directly-Follows Graphs: Balancing Risk and Utility in Process Mining". arXiv preprint arXiv:2012.01119 (2020)
```


### Prerequisite
The main dependencies are [pm4py](https://pm4py.fit.fraunhofer.de/), [diffprivlib](https://github.com/IBM/differential-privacy-library), [multiprocessing](https://pypi.org/project/multiprocess/) and [statistics](https://pypi.org/project/statistics/)
You can install all the requirements with:
```
pip install -r requirements.txt
```
The code was tested with ```python 3.7```.

###Example Usage
An example of the usage of Amun can be found in the file ```run_example.py```.
To perform the execution time experiment, you can use the file ```run_example_execution_time.py```. 
An implementation of Amun with a single thread could be found in the branch ```amun-model```.


