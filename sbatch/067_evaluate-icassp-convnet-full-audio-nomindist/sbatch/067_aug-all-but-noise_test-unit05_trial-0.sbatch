#!/bin/bash

#BATCH --job-name=067_aug-all-but-noise_test-unit05_trial-0
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --mem=64GB
#SBATCH --output=../slurm/slurm_067_aug-all-but-noise_test-unit05_trial-0_%j.out

module purge

# The argument is the kind of data augmentation.
python ../../../src/067_evaluate-icassp-convnet-full-audio-nomindist.py all-but-noise unit05 0