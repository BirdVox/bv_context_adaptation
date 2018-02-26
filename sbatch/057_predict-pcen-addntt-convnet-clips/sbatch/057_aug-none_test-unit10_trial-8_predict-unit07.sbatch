#!/bin/bash

#BATCH --job-name=057_aug-none_test-unit10_trial-8_predict-unit07
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:20:00
#SBATCH --mem=500MB
#SBATCH --output=../slurm/slurm_057_aug-none_test-unit10_trial-8_predict-unit07_%j.out

module purge

# The first argument is the kind of augmentation.
# The second argument is the name of the test unit.
# The third argument is name of trial.
# The fourth argument is the name of the prediction unit.
python ../../../src/057_predict-pcen-addntt-convnet-clips.py none unit10 trial-8 unit07