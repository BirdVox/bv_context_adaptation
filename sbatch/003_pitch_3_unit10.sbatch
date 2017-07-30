#!/bin/bash

#BATCH --job-name=003_pitch_3_unit10
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=2:00:00
#SBATCH --mem=4GB
#SBATCH --output=slurm_003_pitch_3_unit10_%j.out

module purge
module load rubberband/intel/1.8.1

# The first argument is the name of the augmentation.
# The second argument is the instance ID of the augmentation.
# The third argument is the name of the recording unit.
python ../src/003_augment-clips.py pitch 3 unit10