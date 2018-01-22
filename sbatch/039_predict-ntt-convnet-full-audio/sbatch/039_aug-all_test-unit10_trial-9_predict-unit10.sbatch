#!/bin/bash

#BATCH --job-name=039_aug-all_test-unit10_trial-9_predict-unit10
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=48:00:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/039_aug-all_test-unit10_trial-9_predict-unit10_%j.out

module purge

# The first argument is the kind of augmentation.
# The second argument is the name of the test unit.
# The third argument is name of trial.
# The fourth argument is the name of the prediction unit.
python ../../../src/039_predict-ntt-convnet-full-audio.py all unit10 trial-9 unit10