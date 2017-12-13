#!/bin/bash

#BATCH --job-name=037_aug-all-but-noise_unit02_trial-6
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=12:00:00
#SBATCH --mem=8GB
#SBATCH --output=../slurm/slurm_037_aug-all-but-noise_unit02_trial-6_%j.out

module purge

# The first argument is the name of the recording unit.
# The second argument is the duration of background.
python ../../../src/037_train-add-convnet.py all-but-noise unit02 6