#!/bin/bash

#BATCH --job-name=034_aug-noise_test-unit03_trial-9
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=72:00:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/slurm_034_aug-noise_test-unit03_trial-9_%j.out

module purge

# The argument is the kind of data augmentation.
python ../../../src/034_evaluate-pcen-convnet-full-audio.py noise unit03 9