"""In this file, we build the shell jobs to run on the slurm HPC"""
import os
import subprocess
import time

dir_path = os.path.dirname(os.path.realpath(__file__))
jobs_dir = "jobs"

# datasets=["BPIC12","BPIC13","BPIC15","BPIC17","BPIC18","BPIC19","BPIC20","CCC19","CreditReq","Hospital","Sepsis","Traffic"]
datasets=["BPIC12","BPIC13","BPIC19","BPIC20"]
parameters=[0.01,0.05, 0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

""" A  time  limit  of  zero  requests  that no time limit be imposed.  Acceptable time
              formats    include    "minutes",    "minutes:seconds",     "hours:minutes:seconds",
              "days-hours", "days-hours:minutes" and "days-hours:minutes:seconds".
              """

for data in datasets:
    if data in ["BPIC19", "BPIC18"]:
        memory = 32
        exec_time="4-00" # 4 days
    elif data in [ "Traffic", "BPIC17"]:
        memory = 15
        exec_time="16:00:00" # 16 hours
    else:
        memory = 4
        exec_time="01:00:00" # 1 hour
    for parameter in parameters:
        job_name = os.path.join(jobs_dir,"job_%s_%s.sh" % (data, parameter))
        job_log_name =os.path.join(jobs_dir,"log_%s_%s.sh" % (data, parameter))

        with open(job_name, "w") as fout:
            fout.write("#!/bin/bash\n")
            fout.write("#SBATCH --output=jobs/log_%s_%s.txt\n" % (data, parameter))
            fout.write("#SBATCH --mem=%sGB\n" % memory)
            fout.write("#SBATCH --ntasks=1\n")  ## Run on a single CPU
            fout.write("#SBATCH --cpus-per-task=12\n")  # 8 cores per cpu
            fout.write("#SBATCH --partition=main\n")
            fout.write("#SBATCH --time=%s\n" % (exec_time))
            # fout.write("cd ..\n")
            fout.write("python -u %s \"%s\" %s\n" % ('"'+os.path.join(dir_path,"run_experiment_slurm.py")+'"', data, parameter))  # hyper_param_optim

        time.sleep(1)
        subprocess.Popen(("sbatch %s" % job_name).split())