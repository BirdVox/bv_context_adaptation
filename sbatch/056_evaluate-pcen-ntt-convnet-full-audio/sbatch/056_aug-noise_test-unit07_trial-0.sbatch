#!/bin/bash

#BATCH --job-name=056_aug-noise_test-unit07_trial-0
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:30:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/slurm_056_aug-noise_test-unit07_trial-0_%j.out

module purge

# The argument is the kind of data augmentation.
python ../../../src/056_evaluate-pcen-ntt-convnet-full-audio.py noise unit07 0