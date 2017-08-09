#!/bin/bash

#BATCH --job-name=011
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=1:00:00
#SBATCH --mem=16GB
#SBATCH --output=slurm_011_%j.out

module purge

python ../src/011_evaluate-oldbird-per-unit.py
