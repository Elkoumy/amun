"""In this file, we build the shell jobs to run on the slurm HPC"""
import os
import subprocess
import time

jobs_dir = "jobs"

datasets=["Sepsis"]
parameters=[0.1]

for data in datasets:
    if data in ["Hospital", "Traffic", "BPIC17", "BPIC19", "BPIC18"]:
        memory = 15
        exec_time="8-00"
    else:
        memory = 4
        exec_time="1-00"
    for parameter in parameters:
        job_name = os.path.join(jobs_dir,"job_%s_%s.sh" % (data, parameter))
        job_log_name =os.path.join(jobs_dir,"log_%s_%s.sh" % (data, parameter))

        with open(job_name, "w") as fout:
            fout.write("#!/bin/bash\n")
            fout.write("#SBATCH --output=jobs/log_%s_%s.txt\n" % (data, parameter))
            fout.write("#SBATCH --mem=%sGB\n" % memory)
            fout.write("#SBATCH --ntasks=1\n")  ## Run on a single CPU
            fout.write("#SBATCH --cpus-per-task=12\n")  # 8 cores per cpu
            fout.write("#SBATCH --partition=amd\n")
            fout.write("#SBATCH --time=%s\n" % (exec_time))
            fout.write("cd ..\n")
            fout.write("python -u %s \"%s\" %s\n" % ("run_experiment_slurm.py", data, parameter))  # hyper_param_optim

        time.sleep(1)
        subprocess.Popen(("sbatch %s" % job_name).split())