#!/bin/bash

#BATCH --job-name=063_aug-none_test-unit03_trial-7_predict-unit01
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=96:00:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/063_aug-none_test-unit03_trial-7_predict-unit01_%j.out

module purge

# The first argument is the kind of augmentation.
# The second argument is the name of the test unit.
# The third argument is name of trial.
# The fourth argument is the name of the prediction unit.
python ../../../src/063_predict-pcen-deepcontext-convnet-full-audio.py none unit03 trial-7 unit01