#!/bin/bash

#BATCH --job-name=035_aug-all_unit05_trial-1
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=12:00:00
#SBATCH --mem=8GB
#SBATCH --output=../slurm/slurm_035_aug-all_unit05_trial-1_%j.out

module purge

# The first argument is the name of the recording unit.
# The second argument is the duration of background.
python ../../../src/035_train-ntt-convnet.py all unit05 1