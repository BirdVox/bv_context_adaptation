#!/bin/bash

#BATCH --job-name=029_stretch_3_unit07
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=8:00:00
#SBATCH --mem=500MB
#SBATCH --output=../slurm/slurm_029_stretch_3_unit07_%j.out

module purge

# The first argument is the name of the augmentation.
# The second argument is the instance ID of the augmentation.
# The third argument is the name of the recording unit.
python ../../../src/029_compute-clip-pcen.py stretch 3 unit07