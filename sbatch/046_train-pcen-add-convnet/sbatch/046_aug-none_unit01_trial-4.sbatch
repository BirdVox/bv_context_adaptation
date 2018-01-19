#!/bin/bash

#BATCH --job-name=046_aug-none_unit01_trial-4
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=6:00:00
#SBATCH --mem=8GB
#SBATCH --output=../slurm/slurm_046_aug-none_unit01_trial-4_%j.out

module purge

# The first argument is the name of the recording unit.
# The second argument is the duration of background.
python ../../../src/046_train-pcen-add-convnet.py none unit01 4