#!/bin/bash

#BATCH --job-name=035_aug-none_unit10_trial-4
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=12:00:00
#SBATCH --mem=8GB
#SBATCH --output=../slurm/slurm_035_aug-none_unit10_trial-4_%j.out

module purge

# The first argument is the name of the recording unit.
# The second argument is the duration of background.
python ../../../src/035_train-ntt-convnet.py none unit10 4