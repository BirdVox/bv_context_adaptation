#!/bin/bash

#BATCH --job-name=007_unit10
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=1:00:00
#SBATCH --mem=1GB
#SBATCH --output=slurm_007_unit10_%j.out

module purge

# The argument is the name of the recording unit.
python ../src/007_evaluate-skm.py unit10