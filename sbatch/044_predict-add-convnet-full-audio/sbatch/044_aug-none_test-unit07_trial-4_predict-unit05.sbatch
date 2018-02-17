#!/bin/bash

#BATCH --job-name=044_aug-none_test-unit07_trial-4_predict-unit05
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/044_aug-none_test-unit07_trial-4_predict-unit05_%j.out

module purge

# The first argument is the kind of augmentation.
# The second argument is the name of the test unit.
# The third argument is name of trial.
# The fourth argument is the name of the prediction unit.
python ../../../src/044_predict-add-convnet-full-audio.py none unit07 trial-4 unit05