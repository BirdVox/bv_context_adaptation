#!/bin/bash

#BATCH --job-name=025_unit10_trial-4
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=4:00:00
#SBATCH --mem=8GB
#SBATCH --output=../slurm/slurm_025_unit10_trial-4_%j.out

module purge

# The first argument is the name of the recording unit.
# The second argument is the name of the trial.
python ../../../src/025_predict-svm-full-audio.py unit10 04