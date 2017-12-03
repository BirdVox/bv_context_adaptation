#!/bin/bash

#BATCH --job-name=035_all-but-noise_unit02_trial-2
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=4:00:00
#SBATCH --mem=8GB
#SBATCH --gres=gpu:1
#SBATCH --output=../slurm/slurm_035_all-but-noise_unit02_trial-2_%j.out

module purge

# The first argument is the name of the recording unit.
# The second argument is the duration of background.
python ../../../src/035_train-ntt-convnet.py all-but-noise unit02 trial-2