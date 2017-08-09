#!/bin/bash

#BATCH --job-name=012
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=1:00:00
#SBATCH --mem=1GB
#SBATCH --output=slurm_012_%j.out

module purge

python ../src/012_summarize-oldbird-evaluation.py
