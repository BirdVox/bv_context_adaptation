#!/bin/bash

#BATCH --job-name=009_unit10
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=2:00:00
#SBATCH --mem=32GB
#SBATCH --output=slurm_009_unit10_%j.out

module purge

# The argument is the name of the recording unit.
python ../src/009_run-oldbird.py unit10