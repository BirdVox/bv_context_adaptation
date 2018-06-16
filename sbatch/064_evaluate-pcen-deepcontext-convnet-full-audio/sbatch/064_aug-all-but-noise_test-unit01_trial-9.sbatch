#!/bin/bash

#BATCH --job-name=064_aug-all-but-noise_test-unit01_trial-9
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/slurm_064_aug-all-but-noise_test-unit01_trial-9_%j.out

module purge

# The argument is the kind of data augmentation.
python ../../../src/064_evaluate-pcen-deepcontext-convnet-full-audio.py all-but-noise unit01 9