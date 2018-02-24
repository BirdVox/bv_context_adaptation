#!/bin/bash

#BATCH --job-name=055_aug-noise_test-unit01_trial-8
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=20:00:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/slurm_055_aug-noise_test-unit01_trial-8_%j.out

module purge

# The argument is the kind of data augmentation.
python ../../../src/055_evaluate-pcen-ntt-convnet-full-audio.py noise unit01 8