#!/bin/bash

#BATCH --job-name=035_aug-none_unit03_trial-1
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=6:00:00
#SBATCH --mem=8GB
#SBATCH --output=../slurm/slurm_035_aug-none_unit03_trial-1_%j.out

module purge

# The first argument is the name of the recording unit.
# The second argument is the duration of background.
python ../../../src/035_train-dot-convnet.py none unit03 1