#!/bin/bash

#BATCH --job-name=005_stretch_2_unit07
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=3:00:00
#SBATCH --mem=1GB
#SBATCH --output=slurm_005_stretch_2_unit07_%j.out

module purge

# The first argument is the name of the augmentation.
# The second argument is the instance ID of the augmentation.
# The third argument is the name of the recording unit.
python ../src/005_compute-logmelspec.py stretch 2 unit07