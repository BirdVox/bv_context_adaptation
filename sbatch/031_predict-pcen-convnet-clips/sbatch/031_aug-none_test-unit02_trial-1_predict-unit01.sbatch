#!/bin/bash

#BATCH --job-name=031_aug-none_test-unit02_trial-1_predict-unit01
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:10:00
#SBATCH --mem=500MB
#SBATCH --output=../slurm/slurm_031_aug-none_test-unit02_trial-1_predict-unit01_%j.out

module purge

# The first argument is the kind of augmentation.
# The second argument is the name of the test unit.
# The third argument is name of trial.
# The fourth argument is the name of the prediction unit.
python ../../../src/031_predict-pcen-convnet-clips.py none unit02 trial-1 unit01