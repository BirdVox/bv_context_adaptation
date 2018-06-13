#!/bin/bash

#BATCH --job-name=063_aug-all-but-noise_test-unit01_trial-1_predict-unit07
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=96:00:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/063_aug-all-but-noise_test-unit01_trial-1_predict-unit07_%j.out

module purge

# The first argument is the kind of augmentation.
# The second argument is the name of the test unit.
# The third argument is name of trial.
# The fourth argument is the name of the prediction unit.
python ../../../src/063_predict-pcen-deepcontext-convnet-full-audio.py all-but-noise unit01 trial-1 unit07