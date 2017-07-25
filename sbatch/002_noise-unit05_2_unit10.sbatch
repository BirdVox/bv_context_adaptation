#!/bin/bash

#BATCH --job-name=002_noise-unit05_2_unit10
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=2:00:00
#SBATCH --mem=4GB
#SBATCH --output=slurm_002_noise-unit05_2_unit10_%j.out

module purge

# The first argument is the name of the augmentation.
# The first argument is the instance ID of the augmentation.
# The third argument is the ID of the recording unit.
python ../src/002_augment.py noise-unit05 2 10