#!/bin/bash

#BATCH --job-name=020_pitch_1_unit02
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=3:00:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/slurm_020_pitch_1_unit02_%j.out

module purge

# The first argument is the name of the augmentation.
# The second argument is the instance ID of the augmentation.
# The third argument is the name of the recording unit.
python ../../../src/020_compute-skm-logmelspec.py pitch 1 unit02