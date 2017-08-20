#!/bin/bash

#BATCH --job-name=016_unit01
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=4:00:00
#SBATCH --mem=8GB
#SBATCH --output=slurm_016_unit01_%j.out

module purge

# The argument is the name of the recording unit.
python ../src/016_run-spectral-flux.py unit01