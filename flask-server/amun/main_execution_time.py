"""In this file, we build the shell jobs to run on the slurm HPC"""
import os
import subprocess
import time
from amun.amun.guessing_advantage import  AggregateType
dir_path = os.path.dirname(os.path.realpath(__file__))
jobs_dir = "jobs"

# datasets=["BPIC12","BPIC13","BPIC15","BPIC17","BPIC18","BPIC19","BPIC20","CCC19","CreditReq","Hospital","Sepsis","Traffic","Unrineweginfectie", "BPIC14"]
# datasets=["CCC19","Sepsis","Unrineweginfectie", "BPIC14","Traffic","Hospital","CreditReq","BPIC20","BPIC12","BPIC13","BPIC15","BPIC17","BPIC18","BPIC19"]
datasets=["BPIC19"]
# datasets=["BPIC14"]
# datasets=["Sepsis"]
parameters=[0.01]
aggregate_types = [AggregateType.SUM]
input_values=["delta","alpha"]

""" A  time  limit  of  zero  requests  that no time limit be imposed.  Acceptable time
              formats    include    "minutes",    "minutes:seconds",     "hours:minutes:seconds",
              "days-hours", "days-hours:minutes" and "days-hours:minutes:seconds".
              """
# modes = ["pruning", "nonpruning"]
modes =["nonpruning"]
memory = 4
exec_time="01:00:00" # 1 hour
for data in datasets:
    for mode in modes:
        for aggregate_type in aggregate_types:
            for input_value in input_values:
                if mode == "pruning":
                    if data in ["BPIC19", "BPIC18"]:
                        memory = 32
                        exec_time="4-00" # 4 days
                    elif data in [ "Traffic", "BPIC17"]:
                        memory = 15
                        exec_time="4-00" # 4 days
                    elif data in ["BPIC12"]:
                        memory =4
                        exec_time="04:00:00" # 4 hours
                    else:
                        memory = 4
                        exec_time="01:00:00" # 1 hour
                elif mode =="nonpruning":
                    if data in ["BPIC18"]:
                        memory = 32
                        exec_time = "2-01"  # 2 days
                    elif data in ["BPIC19"]:
                        memory = 32
                        exec_time = "1-01"  # 25 hours
                    elif data in ["Traffic", "BPIC17"]:
                        memory = 15
                        exec_time = "20:00:00"  # 20 hours
                    elif data in ["CreditReq", ""]:
                        memory = 8
                        exec_time = "04:00:00"  # 1 days
                    elif data in ["BPIC12", "BPIC13", "BPIC14"]:
                        memory = 4
                        exec_time = "01:00:00"  # 1 hour
                    elif data in ["BPIC20"]:
                        memory = 4
                        exec_time = "00:30:00"  # 30 minutes
                    else:
                        memory = 4
                        exec_time = "00:20:00"  # 20 minutes

                for parameter in parameters:
                    job_name = os.path.join(jobs_dir,"t_job_%s_%s_%s_%s_%s.sh" % (data, parameter,mode,aggregate_type,input_value))
                    job_log_name =os.path.join(jobs_dir,"time_log_%s_%s_%s_%s_%s.txt" % (data, parameter,mode,aggregate_type,input_value))

                    with open(job_name, "w") as fout:
                        fout.write("#!/bin/bash\n")
                        fout.write("#SBATCH --output=jobs/time_log_%s_%s_%s_%s_%s.txt\n" % (data, parameter,mode,aggregate_type,input_value))
                        fout.write("#SBATCH --mem=%sGB\n" % memory)
                        fout.write("#SBATCH --ntasks=1\n")  ## Run on a single CPU
                        #fout.write("#SBATCH --cpus-per-task=12\n")  # 8 cores per cpu
                        # the long cluster has minimum 7 days limit
                        # if data=="Traffic":
                        #     fout.write("#SBATCH --partition=main\n")
                        # else:
                        fout.write("#SBATCH --partition=main\n")
                        fout.write("#SBATCH --time=%s\n" % (exec_time))
                        fout.write("load python-3.7.1\n")
                        # fout.write("cd ..\n")
                        fout.write("python -u %s \"%s\" %s \"%s\" \"%s\" \"%s\" \n" % ('"'+os.path.join(dir_path,"execution_time_experiment.py")+'"', data, parameter,mode, aggregate_type,input_value))  # hyper_param_optim

                    time.sleep(1)
                    subprocess.Popen(("sbatch %s" % job_name).split())