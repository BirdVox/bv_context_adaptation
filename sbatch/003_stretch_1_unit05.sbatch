#!/bin/bash

#BATCH --job-name=003_stretch_1_unit05
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=2:00:00
#SBATCH --mem=4GB
#SBATCH --output=slurm_003_stretch_1_unit05_%j.out

module purge

# The first argument is the name of the augmentation.
# The second argument is the instance ID of the augmentation.
# The third argument is the name of the recording unit.
python ../src/003_augment.py stretch 1 unit05