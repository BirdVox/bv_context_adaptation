#!/bin/bash

#BATCH --job-name=018_aug-stretch_test-unit03_trial-0
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/slurm_018_aug-stretch_test-unit03_trial-0_%j.out

module purge

# The argument is the kind of data augmentation.
python ../../../src/018_evaluate-icassp-convnet-full-audio.py stretch unit03 0