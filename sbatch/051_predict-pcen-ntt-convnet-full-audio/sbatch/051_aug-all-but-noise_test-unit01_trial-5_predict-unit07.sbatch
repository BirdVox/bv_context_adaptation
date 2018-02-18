#!/bin/bash

#BATCH --job-name=051_aug-all-but-noise_test-unit01_trial-5_predict-unit07
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=96:00:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/051_aug-all-but-noise_test-unit01_trial-5_predict-unit07_%j.out

module purge

# The first argument is the kind of augmentation.
# The second argument is the name of the test unit.
# The third argument is name of trial.
# The fourth argument is the name of the prediction unit.
python ../../../src/051_predict-pcen-ntt-convnet-full-audio.py all-but-noise unit01 trial-5 unit07