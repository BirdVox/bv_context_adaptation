#!/bin/bash

#BATCH --job-name=039_aug-none_test-unit01_trial-3_predict-unit01
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/039_aug-none_test-unit01_trial-3_predict-unit01_%j.out

module purge

# The first argument is the kind of augmentation.
# The second argument is the name of the test unit.
# The third argument is name of trial.
# The fourth argument is the name of the prediction unit.
python ../../../src/039_predict-add-convnet-full-audio.py none unit01 trial-3 unit01