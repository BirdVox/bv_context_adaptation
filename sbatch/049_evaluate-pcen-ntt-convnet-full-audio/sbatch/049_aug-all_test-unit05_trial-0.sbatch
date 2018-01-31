#!/bin/bash

#BATCH --job-name=049_aug-all_test-unit05_trial-0
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:30:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/slurm_049_aug-all_test-unit05_trial-0_%j.out

module purge

# The argument is the kind of data augmentation.
python ../../../src/049_evaluate-pcen-ntt-convnet-full-audio.py all unit05 0