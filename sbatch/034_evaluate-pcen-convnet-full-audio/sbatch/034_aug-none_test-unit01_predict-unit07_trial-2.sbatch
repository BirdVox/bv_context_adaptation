#!/bin/bash

#BATCH --job-name=034_aug-none_test-unit01_predict-unit07_trial-2
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:05:00
#SBATCH --mem=100MB
#SBATCH --output=../slurm/slurm_034_aug-none_test-unit01_predict-unit07_trial-2_%j.out

module purge

# The first argument is the kind of data augmentation.
# The second argument is the test unit.
# The third argument is the prediction unit.
# The fourth argument is the trial index.
python ../../../src/034_evaluate-pcen-convnet-full-audio.py none unit01 unit07 2