#!/bin/bash
#SBATCH --output=test_parallel_log.txt
#SBATCH --mem=4GB
#SBATCH --ntasks=4
#SBATCH --partition=main
#SBATCH --time=02:00:00
module load python-3.7.1
python -u "/gpfs/hpc/home/elkoumy/amun/test_parallel.py"