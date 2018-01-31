#!/bin/bash

#BATCH --job-name=016_unit10
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:10:00
#SBATCH --mem=1GB
#SBATCH --output=slurm_016_unit10_%j.out

module purge

# The argument is the name of the recording unit.
python ../src/053_evaluate-spectral-flux.py unit10