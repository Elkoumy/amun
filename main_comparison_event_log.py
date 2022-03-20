import pandas as pd
import os
import time
import subprocess

def generate_jobs(mode,org_path, anonymized_dir, comparison_dir,dataset,engine,anonymized_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    jobs_dir = "comp_jobs"
    memory = 16
    exec_time = "04:00:00"  # 12 hour

    if dataset in ["BPIC12_t", "Hospital_t", "BPIC15_t", "Traffic_t",
                "BPIC20_t", "BPIC17_t"]:
        exec_time = "10:00:00"  # 1 day
        if dataset in ["Traffic_t"]:
            memory = 32
    elif dataset in ["Hospital_t","BPIC14_t", "BPIC19_t", "BPIC18_t"]:
        exec_time = "24:00:00"  # 1 day
        if engine=="amun" and mode=="emd" and dataset in ["BPIC14_t","BPIC19_t", "BPIC18_t"]:
            memory=32

    job_name = os.path.join(jobs_dir, "comp_%s_%s_%s_%s.sh" % (mode, dataset, engine, anonymized_name))
    job_log_name = os.path.join(jobs_dir, "comp_%s_%s_%s_%s.txt" % (mode, dataset, engine, anonymized_name))
    with open(job_name, "w") as fout:
        fout.write("#!/bin/bash\n")
        fout.write("#SBATCH --output=comp_jobs/comp_%s_%s_%s_%s.txt" % (mode, dataset, engine, anonymized_name))
        fout.write("#SBATCH --mem=%sGB\n" % memory)
        fout.write("#SBATCH --ntasks=1\n")  ## Run on a single CPU
        # fout.write("#SBATCH --cpus-per-task=12\n")  # 8 cores per cpu
        fout.write("#SBATCH --partition=amd\n")
        fout.write("#SBATCH --time=%s\n" % (exec_time))
        # fout.write("module load python-3.7.1\n")
        fout.write("module load python/3.8.6\n")
        # fout.write("cd ..\n")

        # dataset = os.sys.argv[1]
        # delta = os.sys.argv[2]
        # precision = os.sys.argv[3]
        # iteration = os.sys.argv[4]
        fout.write("python -u %s \"%s\" \"%s\" \"%s\" \"%s\" \n"
                   % ('"' + os.path.join(dir_path, "run_event_log_comparison_slurm.py") + '"',
                      mode,
                      org_path,
                      anonymized_dir,
                      comparison_dir))
    time.sleep(1)
    subprocess.Popen(("sbatch %s" % job_name).split())

if __name__ == "__main__":
    # datasets = ["CCC19_t", "Sepsis_t", "Unrineweginfectie_t", "BPIC14_t", "Traffic_t", "Hospital_t", "CreditReq_t",
    #             "BPIC20_t",
    #             "BPIC12_t", "BPIC13_t", "BPIC15_t", "BPIC17_t", "BPIC18_t", "BPIC19_t"]

    # datasets = ["CCC19_t", "Unrineweginfectie_t", "BPIC14_t", "Traffic_t", "Hospital_t", "CreditReq_t",
    #             "BPIC20_t",
    #             "BPIC12_t", "BPIC13_t", "BPIC15_t", "BPIC17_t", "BPIC18_t", "BPIC19_t"]
    datasets=["Sepsis_t","BPIC20_t"]
    dir_path = os.path.dirname(os.path.realpath(__file__))
    comparison_dir = os.path.join(dir_path, "comparison")
    # amun_dir = os.path.join(dir_path, "anonymized_logs", "amun")
    amun_dir=os.path.join(dir_path,"anonymized_logs","amun_sub")
    # pripel_trace_dir = os.path.join(dir_path, "anonymized_logs", "pripel","trace_variant")
    # pripel_time_dir = os.path.join(dir_path, "anonymized_logs", "pripel","time")
    pripel_trace_dir = os.path.join(dir_path, "anonymized_logs", "pripel")
    pripel_time_dir = os.path.join(dir_path, "anonymized_logs", "pripel")
    libra_dir=os.path.join(dir_path, "anonymized_logs", "libra")
    sacofa_dir=os.path.join(dir_path, "anonymized_logs", "sacofa")

    for dataset in datasets:
        org_path=os.path.join(dir_path,"data",dataset+".xes")
        # files=list(os.walk(amun_dir))[0][2]
        # for log in files:
        #     if log.find(dataset)!=-1:
        #         """Amun"""
        #         anonymized_dir=os.path.join(amun_dir,log)
        #         generate_jobs("emd", org_path, anonymized_dir, comparison_dir, dataset, "amun", log)
        #         generate_jobs("jaccard", org_path, anonymized_dir, comparison_dir, dataset, "amun", log)
        #         compare_emd(org_path,anonymized_dir,comparison_dir)
        #         compare_jaccard(org_path, anonymized_dir, comparison_dir)

        """Pripel"""
        files = list(os.walk(pripel_trace_dir))[0][2]

        for log in files:
            if log.find(dataset)!=-1:
                anonymized_dir = os.path.join(pripel_trace_dir, log)
                generate_jobs("jaccard", org_path, anonymized_dir, comparison_dir, dataset, "pripel", log)
                generate_jobs("emd", org_path, anonymized_dir, comparison_dir, dataset, "pripel", log)
                # compare_jaccard(org_path, anonymized_dir, comparison_dir)

        """SaCoFa"""
        files = list(os.walk(pripel_time_dir))[0][2]
        for log in files:
            if log.find(dataset)!=-1:
                anonymized_dir = os.path.join(sacofa_dir, log)
                generate_jobs("jaccard", org_path, anonymized_dir, comparison_dir, dataset, "sacofa", log)
                generate_jobs("emd", org_path, anonymized_dir, comparison_dir, dataset, "sacofa", log)
                # compare_emd(org_path, anonymized_dir, comparison_dir)

        """Libra"""
        anonymized_dir = os.path.join(libra_dir, log)
        generate_jobs("emd", org_path, anonymized_dir, comparison_dir, dataset, "libra", log)
        generate_jobs("jaccard", org_path, anonymized_dir, comparison_dir, dataset, "libra", log)