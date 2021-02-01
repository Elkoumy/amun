"""In this file, we build the shell jobs to run on the slurm HPC"""
import os
import subprocess
import time
from amun.guessing_advantage import  AggregateType
dir_path = os.path.dirname(os.path.realpath(__file__))
jobs_dir = "jobs"




""" A  time  limit  of  zero  requests  that no time limit be imposed.  Acceptable time
              formats    include    "minutes",    "minutes:seconds",     "hours:minutes:seconds",
              "days-hours", "days-hours:minutes" and "days-hours:minutes:seconds".
              """
datasets = ["CCC19_t", "Sepsis_t", "Unrineweginfectie_t", "BPIC14_t", "Traffic_t", "Hospital_t", "CreditReq_t", "BPIC20_t",
                "BPIC12_t", "BPIC13_t", "BPIC15_t", "BPIC17_t", "BPIC18_t", "BPIC19_t"]

datasets = ["BPIC17_t", "BPIC19_t"]
memory = 4
exec_time="01:00:00" # 1 hour
number_of_experiments =10
# number_of_experiments =70
for data in datasets:

    if data in ["CCC19_t","Unrineweginfectie_t"]:
        memory = 4
        exec_time = "00:5:00"  # 5 minutes
    elif data in ["Sepsis_t","Traffic_t", "Hospital_t", "CreditReq_t"]:
        memory = 16
        exec_time = "00:20:00"  # 20 minutes
    elif data in ["BPIC14_t","BPIC20_t","BPIC12_t", "BPIC13_t", "BPIC15_t"]:
        memory = 16
        exec_time = "00:40:00"  # 40 minutes
    elif data in ["BPIC17_t", "BPIC18_t", "BPIC19_t"]:
        memory = 32
        exec_time = "03:00:00"  # 3 hours


    job_name = os.path.join(jobs_dir,"job_%s.sh" % (data))
    job_log_name =os.path.join(jobs_dir,"log_%s.txt" % (data))

    with open(job_name, "w") as fout:
        fout.write("#!/bin/bash\n")
        fout.write("#SBATCH --output=jobs/log_%s.txt\n" % (data))
        fout.write("#SBATCH --mem=%sGB\n" % memory)
        fout.write("#SBATCH --ntasks=1\n")  ## Run on a single CPU
        #fout.write("#SBATCH --cpus-per-task=12\n")  # 8 cores per cpu
        fout.write("#SBATCH --partition=amd\n")
        fout.write("#SBATCH --time=%s\n" % (exec_time))
        fout.write("module load python-3.7.1\n")
        # fout.write("cd ..\n")
        fout.write("python -u %s \"%s\" \n" % ('"'+os.path.join(dir_path,"run_event_log_anonymizer_slurm.py")+'"',data))

    time.sleep(1)
    subprocess.Popen(("sbatch %s" % job_name).split())