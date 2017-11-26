#!/bin/bash

#BATCH --job-name=031_aug-none_test-unit03_trial-9_predict-unit03
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=4:00:00
#SBATCH --mem=500MB
#SBATCH --output=../slurm/slurm_031_aug-none_test-unit03_trial-9_predict-unit03_%j.out.out

module purge

# The first argument is the kind of augmentation.
# The second argument is the name of the test unit.
# The third argument is name of trial.
# The fourth argument is the name of the prediction unit.
python ../../../src/031_predict-pcen-convnet-clips.py none unit03 trial-9 unit03