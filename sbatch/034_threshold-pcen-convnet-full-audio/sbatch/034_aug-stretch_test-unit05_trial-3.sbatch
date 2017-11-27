#!/bin/bash

#BATCH --job-name=034_aug-stretch_test-unit05_trial-3
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:30:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/slurm_034_aug-stretch_test-unit05_trial-3_%j.out

module purge

# The argument is the kind of data augmentation.
python ../../../src/034_threshold-pcen-convnet-full-audio.py stretch unit05 3