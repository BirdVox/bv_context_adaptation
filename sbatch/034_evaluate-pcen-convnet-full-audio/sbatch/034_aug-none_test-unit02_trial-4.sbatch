#!/bin/bash

#BATCH --job-name=034_aug-none_test-unit02_trial-4
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=8:00:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/slurm_034_aug-none_test-unit02_trial-4_%j.out

module purge

# The argument is the kind of data augmentation.
python ../../../src/034_evaluate-pcen-convnet-full-audio.py none unit02 4