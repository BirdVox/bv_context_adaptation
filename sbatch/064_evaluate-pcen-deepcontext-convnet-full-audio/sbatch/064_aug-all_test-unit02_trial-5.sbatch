#!/bin/bash

#BATCH --job-name=064_aug-all_test-unit02_trial-5
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/slurm_064_aug-all_test-unit02_trial-5_%j.out

module purge

# The argument is the kind of data augmentation.
python ../../../src/064_evaluate-pcen-deepcontext-convnet-full-audio.py all unit02 5