#!/bin/bash

#BATCH --job-name=069_aug-none_test-unit07_trial-0
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --mem=64GB
#SBATCH --output=../slurm/slurm_069_aug-none_test-unit07_trial-0_%j.out

module purge

# The argument is the kind of data augmentation.
python ../../../src/069_evaluate-pcen-addntt-convnet-full-audio-nomindist.py none unit07 0