#!/bin/bash

#BATCH --job-name=007_unit02
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=2:00:00
#SBATCH --mem=1GB
#SBATCH --output=slurm_007_unit02_%j.out

module purge

# The argument is the name of the recording unit.
python ../src/007_run-oldbird.py unit02