#!/bin/bash

#BATCH --job-name=055_aug-all_test-unit03_trial-1
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=20:00:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/slurm_055_aug-all_test-unit03_trial-1_%j.out

module purge

# The argument is the kind of data augmentation.
python ../../../src/055_evaluate-pcen-ntt-convnet-full-audio.py all unit03 1