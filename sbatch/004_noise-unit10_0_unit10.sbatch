#!/bin/bash

#BATCH --job-name=004_noise-unit10_0_unit10
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:05:00
#SBATCH --mem=1GB
#SBATCH --output=slurm_004_noise-unit10_0_unit10_%j.out

module purge

# The first argument is the name of the augmentation.
# The second argument is the instance ID of the augmentation.
# The third argument is the name of the recording unit.
python ../src/004_save-hdf5.py noise-unit10 0 unit10