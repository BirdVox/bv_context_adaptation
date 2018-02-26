#!/bin/bash

#BATCH --job-name=057_aug-none_test-unit01_trial-9_predict-unit01
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:20:00
#SBATCH --mem=500MB
#SBATCH --output=../slurm/slurm_057_aug-none_test-unit01_trial-9_predict-unit01_%j.out

module purge

# The first argument is the kind of augmentation.
# The second argument is the name of the test unit.
# The third argument is name of trial.
# The fourth argument is the name of the prediction unit.
python ../../../src/057_predict-pcen-addntt-convnet-clips.py none unit01 trial-9 unit01