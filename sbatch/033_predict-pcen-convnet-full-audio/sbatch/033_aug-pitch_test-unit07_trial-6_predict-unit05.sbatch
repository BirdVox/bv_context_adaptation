#!/bin/bash

#BATCH --job-name=033_aug-pitch_test-unit07_trial-6_predict-unit05
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=6:00:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/033_aug-pitch_test-unit07_trial-6_predict-unit05_%j.out

module purge

# The first argument is the kind of augmentation.
# The second argument is the name of the test unit.
# The third argument is name of trial.
# The fourth argument is the name of the prediction unit.
python ../../../src/033_predict-pcen-convnet-full-audio.py pitch unit07 trial-6 unit05