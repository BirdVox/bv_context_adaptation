#!/bin/bash

#BATCH --job-name=018_aug-pitch_test-unit07_trial-8
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:10:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm_018_aug-pitch_test-unit07_trial-8_%j.out

module purge

# The argument is the kind of data augmentation.
python ../../../src/018_evaluate-icassp-convnet-full-audio.py pitch unit07 8