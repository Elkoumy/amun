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

# datasets = ["CCC19_t",  "Unrineweginfectie_t", "Sepsis_t","Traffic_t", "Hospital_t", "CreditReq_t", "BPIC15_t","BPIC20_t", "BPIC13_t",
# "BPIC12_t", "BPIC17_t", "BPIC14_t", "BPIC19_t", "BPIC18_t" ]

datasets = ["CCC19_t",  "Unrineweginfectie_t", "Sepsis_t","Traffic_t", "Hospital_t", "CreditReq_t", "BPIC15_t","BPIC20_t", "BPIC13_t",
"BPIC12_t", "BPIC17_t", "BPIC14_t", "BPIC19_t" ]

datasets =["BPIC18_t"]

memory = 4
exec_time="01:00:00" # 1 hour

# no_of_iterations =9
# start_iteration=8
no_of_iterations =1
start_iteration=0

deltas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]

precisions = [0.1]
deltas=[0.1]

for precision in precisions:
    for delta in deltas:
        for data in datasets:

            for iteration in range(start_iteration, no_of_iterations):
                if data in ["CCC19_t","Unrineweginfectie_t"]:
                    memory = 4
                    exec_time = "00:5:00"  # 1 minutes
                elif data in ["Sepsis_t","Traffic_t","CreditReq_t", "BPIC15_t"]:
                    memory = 16
                    exec_time = "00:14:00"  # 7 minutes
                elif data in [ "Hospital_t"]:
                    memory = 16
                    exec_time = "00:25:00"  # 25 minutes
                elif data in ["BPIC20_t", "BPIC13_t"]:
                    memory = 20
                    exec_time = "01:00:00"  # 30 minutes
                elif data in ["BPIC12_t" ]:
                    memory = 20
                    exec_time = "01:00:00"  # 32 minutes

                elif data in ["BPIC17_t"]:
                    memory = 20
                    exec_time = "02:40:00"  # 40 minutes
                elif data in ["BPIC14_t"]:
                    memory = 24
                    exec_time = "02:30:00"  # 1.5 hours

                elif data in [  "BPIC19_t"]:
                    memory = 32
                    exec_time = "04:00:00"  # 4 hours

                elif data in ["BPIC18_t"]:
                    memory = 42
                    exec_time = "07:00:00"  # 5 hours


                job_name = os.path.join(jobs_dir,"j_%s_%s_%s_%s.sh" % (data, precision, delta, iteration))
                job_log_name =os.path.join(jobs_dir,"l_%s_%s_%s_%s.txt" % (data, precision, delta, iteration))

                with open(job_name, "w") as fout:
                    fout.write("#!/bin/bash\n")
                    fout.write("#SBATCH --output=jobs/l_%s_%s_%s_%s.txt" % (data, precision, delta, iteration))
                    fout.write("#SBATCH --mem=%sGB\n" % memory)
                    fout.write("#SBATCH --ntasks=1\n")  ## Run on a single CPU
                    #fout.write("#SBATCH --cpus-per-task=12\n")  # 8 cores per cpu
                    fout.write("#SBATCH --partition=amd\n")
                    fout.write("#SBATCH --time=%s\n" % (exec_time))
                    #fout.write("module load python-3.7.1\n")
                    # fout.write("cd ..\n")

                    # dataset = os.sys.argv[1]
                    # delta = os.sys.argv[2]
                    # precision = os.sys.argv[3]
                    # iteration = os.sys.argv[4]
                    fout.write("python -u %s \"%s\" %s %s %s \n"
                               %('"'+os.path.join(dir_path,"run_event_log_anonymizer_slurm.py")+'"',
                                                           data,
                                                           delta,
                                                           precision,
                                                           iteration))

                time.sleep(1)
                subprocess.Popen(("sbatch %s" % job_name).split())