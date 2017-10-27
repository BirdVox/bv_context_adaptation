#!/bin/bash

#BATCH --job-name=025_unit02_trial-5
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=4:00:00
#SBATCH --mem=8GB
#SBATCH --output=../slurm/slurm_025_unit02_trial-5_%j.out

module purge

# The first argument is the name of the recording unit.
# The second argument is the name of the trial.
python ../../../src/025_predict-svm-full-audio.py unit02 05