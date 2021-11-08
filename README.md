# Amun
Amun is a framework that leverage recently developed Privacy-Enhancing Technologies (PETs) to help 
organizations publish anonymized process models. The main contributions of the project are listed below.
- Amun uses a mathematically proven privacy model to 
  balance the risk correlated with publishing process models and the utility after anonymization.
  It uses an ε-differential-privacy mechanism to anonymize Directly-Follows Graphs (DFGs).
  It provides a mathematical approach to calculate the value of ε that represents the amount of noise 
  injected a process mining model that optimizes the risk and utility measures. 
  Amun keeps all the traces and all the activities of a DFG. 
  An emperical evaluation of Amun using 13 real-world event logs could be found in our recent [paper](https://arxiv.org/pdf/2012.01119.pdf).
- Amun proposes a framework to anonymize event logs to the extent that no individual can be singled out using the anonymized log. It anonymizes event logs in order to guarantee that, upon the disclosure of the anonymized log, the probability that an attacker may single out any individual represented in the original log, does not increase by more than a threshold. Amun proposes a differentially private disclosure mechanism, which oversamples the cases in the log and adds noise to the timestamps to the extent required to achieve the above privacy guarantee. An emperical evaluation of Amun using 14 real-world event logs could be found in our recent [paper](https://arxiv.org/abs/2103.11739).
### Cite the Project

```
@inproceedings{DBLP:conf/icpm/ElkoumyPD21,
  author    = {Gamal Elkoumy and
               Alisa Pankova and
               Marlon Dumas},
  editor    = {Claudio Di Ciccio and
               Chiara Di Francescomarino and
               Pnina Soffer},
  title     = {Mine Me but Don't Single Me Out: Differentially Private Event Logs
               for Process Mining},
  booktitle = {3rd International Conference on Process Mining, {ICPM} 2021, Eindhoven,
               Netherlands, October 31 - Nov. 4, 2021},
  pages     = {80--87},
  publisher = {{IEEE}},
  year      = {2021},
  url       = {https://doi.org/10.1109/ICPM53251.2021.9576852},
  doi       = {10.1109/ICPM53251.2021.9576852},
  timestamp = {Fri, 29 Oct 2021 16:42:41 +0200},
  biburl    = {https://dblp.org/rec/conf/icpm/ElkoumyPD21.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
  
```

```
@article{DBLP:journals/corr/abs-2012-01119,
  author    = {Gamal Elkoumy and
               Alisa Pankova and
               Marlon Dumas},
  title     = {Privacy-Preserving Directly-Follows Graphs: Balancing Risk and Utility
               in Process Mining},
  journal   = {CoRR},
  volume    = {abs/2012.01119},
  year      = {2020},
  url       = {https://arxiv.org/abs/2012.01119},
  eprinttype = {arXiv},
  eprint    = {2012.01119},
  timestamp = {Fri, 04 Dec 2020 12:07:23 +0100},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2012-01119.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}

```

### Prerequisite
The main dependencies are: [pm4py](https://pm4py.fit.fraunhofer.de/), [diffprivlib](https://github.com/IBM/differential-privacy-library), [multiprocessing](https://pypi.org/project/multiprocess/) and [statistics](https://pypi.org/project/statistics/)
You can install all the requirements with:
```
pip install -r requirements.txt
```
The code was tested with ```python 3.8.5```.

### Example Usage
To anonymize an event log, place the XES file in the directory ```input_logs```. Then you can run the command
```
python Amun.py Sepsis sampling 0.2
```
Amun assumes that the event log has only the three columns: ```case:concept:name```, ```concept:name```, and ```time:timestamp``` in your XES file.

### Reproduce Emperical Evaluation
An example of the usage of Amun to anonymize DFGs can be found in the file ```run_example.py```.
To perform the execution time experiment, you can use the file ```run_example_execution_time.py```. 
An implementation of Amun with a single thread could be found in the branch ```amun-model```.

To reproduce the emperical evaluation of Amun to anonymize event logs you can use the file ```run_event_log_anonymizer.py```.


