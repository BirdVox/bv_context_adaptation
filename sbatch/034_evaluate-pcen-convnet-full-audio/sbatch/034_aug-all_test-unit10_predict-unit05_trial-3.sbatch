#!/bin/bash

#BATCH --job-name=034_aug-all_test-unit10_predict-unit05_trial-3
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:15:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/slurm_034_aug-all_test-unit10_predict-unit05_trial-3_%j.out

module purge

# The first argument is the kind of data augmentation.
# The second argument is the test unit.
# The third argument is the prediction unit.
# The fourth argument is the trial index.
python ../../../src/034_evaluate-pcen-convnet-full-audio.py all unit10 unit05 3