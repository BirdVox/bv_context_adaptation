#!/bin/bash

#BATCH --job-name=035_aug-all-but-noise_unit05_trial-7
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --mem=8GB
#SBATCH --output=../slurm/slurm_035_aug-all-but-noise_unit05_trial-7_%j.out

module purge

# The first argument is the name of the recording unit.
# The second argument is the duration of background.
python ../../../src/035_train-ntt-convnet.py all-but-noise unit05 7