#!/bin/bash

#BATCH --job-name=056_aug-none_test-unit07_trial-1_predict-unit05
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=96:00:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/056_aug-none_test-unit07_trial-1_predict-unit05_%j.out

module purge

# The first argument is the kind of augmentation.
# The second argument is the name of the test unit.
# The third argument is name of trial.
# The fourth argument is the name of the prediction unit.
python ../../../src/056_predict-pcen-addntt-convnet-full-audio.py none unit07 trial-1 unit05