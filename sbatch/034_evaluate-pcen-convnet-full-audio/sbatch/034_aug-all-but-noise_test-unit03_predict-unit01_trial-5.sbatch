#!/bin/bash

#BATCH --job-name=034_aug-all-but-noise_test-unit03_predict-unit01_trial-5
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:15:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/slurm_034_aug-all-but-noise_test-unit03_predict-unit01_trial-5_%j.out

module purge

# The first argument is the kind of data augmentation.
# The second argument is the test unit.
# The third argument is the prediction unit.
# The fourth argument is the trial index.
python ../../../src/034_evaluate-pcen-convnet-full-audio.py all-but-noise unit03 unit01 5