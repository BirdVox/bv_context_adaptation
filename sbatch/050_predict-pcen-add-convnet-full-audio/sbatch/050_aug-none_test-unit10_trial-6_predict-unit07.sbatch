#!/bin/bash

#BATCH --job-name=050_aug-none_test-unit10_trial-6_predict-unit07
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=96:00:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/050_aug-none_test-unit10_trial-6_predict-unit07_%j.out

module purge

# The first argument is the kind of augmentation.
# The second argument is the name of the test unit.
# The third argument is name of trial.
# The fourth argument is the name of the prediction unit.
python ../../../src/050_predict-pcen-add-convnet-full-audio.py none unit10 trial-6 unit07