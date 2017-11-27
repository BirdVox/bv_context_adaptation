#!/bin/bash

#BATCH --job-name=017_aug-all_test-unit10_trial-3
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:30:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/slurm_017_aug-all_test-unit10_trial-3_%j.out

module purge

# The argument is the kind of data augmentation.
python ../../../src/017_threshold-icassp-convnet-full-audio.py all unit10 3