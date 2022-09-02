# Amun
Amun is a framework that leverage recently developed Privacy-Enhancing Technologies (PETs) to help 
organizations publish anonymized process models. The main contributions of the project are listed below.

- Amun proposes a framework to anonymize event logs to the extent that no individual can be singled out using the anonymized log. It anonymizes event logs in order to guarantee that, upon the disclosure of the anonymized log, the probability that an attacker may single out any individual represented in the original log, does not increase by more than a threshold. Amun proposes a differentially private disclosure mechanism, which oversamples the cases in the log and adds noise to the timestamps to the extent required to achieve the above privacy guarantee. An emperical evaluation of Amun using 14 real-world event logs could be found in our recent [paper](https://ieeexplore.ieee.org/document/9576852).
- Amun uses a mathematically proven privacy model to 
  balance the risk correlated with publishing process models and the utility after anonymization.
  It uses an ε-differential-privacy mechanism to anonymize Directly-Follows Graphs (DFGs).
  It provides a mathematical approach to calculate the value of ε that represents the amount of noise 
  injected a process mining model that optimizes the risk and utility measures. 
  Amun keeps all the traces and all the activities of a DFG. 
  An emperical evaluation of Amun using 13 real-world event logs could be found in our recent [paper](https://arxiv.org/pdf/2012.01119.pdf).


### Installing the Docker Image
First download the repository locally in your machine. Then, build the image using the following command:
```
sudo docker build -f Amun.docker -t amun-app .
```
To run the docker image, please use the following command:
```
sudo docker run --rm -p 3000:3000 amun-app
```

You can now use the application using [http://localhost:3000/](http://localhost:3000/).




