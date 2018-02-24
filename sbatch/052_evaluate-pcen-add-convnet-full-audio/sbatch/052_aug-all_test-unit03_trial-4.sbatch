#!/bin/bash

#BATCH --job-name=052_aug-all_test-unit03_trial-4
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/slurm_052_aug-all_test-unit03_trial-4_%j.out

module purge

# The argument is the kind of data augmentation.
python ../../../src/052_evaluate-pcen-add-convnet-full-audio.py all unit03 4