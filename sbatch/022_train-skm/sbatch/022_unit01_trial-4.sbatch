#!/bin/bash

#BATCH --job-name=022_unit01_trial-4
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=1:00:00
#SBATCH --mem=8GB
#SBATCH --output=../slurm/slurm_022_unit01_trial-4_%j.out

module purge

# The first argument is the name of the recording unit.
# The second argument is the name of the trial.
python ../../../src/022_train-skm.py unit01 04