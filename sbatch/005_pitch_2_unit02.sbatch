#!/bin/bash

#BATCH --job-name=005_pitch_2_unit02
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=3:00:00
#SBATCH --mem=1GB
#SBATCH --output=slurm_005_pitch_2_unit02_%j.out

module purge

# The first argument is the name of the augmentation.
# The second argument is the instance ID of the augmentation.
# The third argument is the name of the recording unit.
python ../src/005_compute-logmelspec.py pitch 2 unit02