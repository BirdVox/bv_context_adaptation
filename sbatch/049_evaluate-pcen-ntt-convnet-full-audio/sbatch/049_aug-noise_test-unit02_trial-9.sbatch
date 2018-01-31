#!/bin/bash

#BATCH --job-name=049_aug-noise_test-unit02_trial-9
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:30:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/slurm_049_aug-noise_test-unit02_trial-9_%j.out

module purge

# The argument is the kind of data augmentation.
python ../../../src/049_evaluate-pcen-ntt-convnet-full-audio.py noise unit02 9