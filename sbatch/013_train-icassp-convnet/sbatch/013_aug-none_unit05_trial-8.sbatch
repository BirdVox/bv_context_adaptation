#!/bin/bash

#BATCH --job-name=013_aug-none_unit05_trial-8
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=6:00:00
#SBATCH --mem=8GB
#SBATCH --output=../slurm/slurm_013_aug-none_unit05_trial-8_%j.out

module purge

# The first argument is the kind of augmentation.
# The second argument is the name of the recording unit.
# The third argument is name of trial.
python ../../../src/013_train-icassp-convnet.py none unit05 trial-8