#!/bin/bash

#BATCH --job-name=065_aug-none_test-unit01_trial-7
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --mem=64GB
#SBATCH --output=../slurm/slurm_065_aug-none_test-unit01_trial-7_%j.out

module purge

# The argument is the kind of data augmentation.
python ../../../src/065_evaluate-pcen-add-convnet-full-audio-nomindist.py none unit01 7