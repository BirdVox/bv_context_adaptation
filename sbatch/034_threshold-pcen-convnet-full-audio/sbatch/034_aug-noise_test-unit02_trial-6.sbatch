#!/bin/bash

#BATCH --job-name=034_aug-noise_test-unit02_trial-6
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:30:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/slurm_034_aug-noise_test-unit02_trial-6_%j.out

module purge

# The argument is the kind of data augmentation.
python ../../../src/034_threshold-pcen-convnet-full-audio.py noise unit02 6