#!/bin/bash

#BATCH --job-name=062_aug-none_unit07_trial-9
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=16:00:00
#SBATCH --mem=8GB
#SBATCH --output=../slurm/slurm_062_aug-none_unit07_trial-9_%j.out

module purge

# The first argument is the name of the recording unit.
# The second argument is the duration of background.
python ../../../src/062_train-pcen-deepcontext-convnet.py none unit07 9