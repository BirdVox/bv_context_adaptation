#!/bin/bash

#BATCH --job-name=002_noise-unit10_3_unit03
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=2:00:00
#SBATCH --mem=4GB
#SBATCH --output=slurm_002_noise-unit10_3_unit03_%j.out

module purge

# The first argument is the name of the augmentation.
# The first argument is the instance ID of the augmentation.
# The third argument is the ID of the recording unit.
python ../src/002_augment.py noise-unit10 3 03