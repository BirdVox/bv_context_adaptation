#!/bin/bash

#BATCH --job-name=054_aug-all-but-noise_unit07_trial-9
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --mem=8GB
#SBATCH --output=../slurm/slurm_054_aug-all-but-noise_unit07_trial-9_%j.out

module purge

# The first argument is the name of the recording unit.
# The second argument is the duration of background.
python ../../../src/054_train-pcen-addntt-convnet.py all-but-noise unit07 9