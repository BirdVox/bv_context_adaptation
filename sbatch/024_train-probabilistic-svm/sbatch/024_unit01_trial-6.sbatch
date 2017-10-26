#!/bin/bash

#BATCH --job-name=024_unit01_trial-6
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=2:00:00
#SBATCH --mem=8GB
#SBATCH --output=../slurm/slurm_024_unit01_trial-6_%j.out

module purge

# The first argument is the name of the recording unit.
# The second argument is the name of the trial.
python ../../../src/024_train-probabilistic-svm.py unit01 06