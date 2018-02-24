#!/bin/bash

#BATCH --job-name=052_aug-noise_test-unit03_trial-0
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/slurm_052_aug-noise_test-unit03_trial-0_%j.out

module purge

# The argument is the kind of data augmentation.
python ../../../src/052_evaluate-pcen-add-convnet-full-audio.py noise unit03 0