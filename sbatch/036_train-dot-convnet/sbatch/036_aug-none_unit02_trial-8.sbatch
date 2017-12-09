#!/bin/bash

#BATCH --job-name=036_aug-none_unit02_trial-8
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=6:00:00
#SBATCH --mem=8GB
#SBATCH --output=../slurm/slurm_036_aug-none_unit02_trial-8_%j.out

module purge

# The first argument is the name of the recording unit.
# The second argument is the duration of background.
python ../../../src/036_train-dot-convnet.py none unit02 8