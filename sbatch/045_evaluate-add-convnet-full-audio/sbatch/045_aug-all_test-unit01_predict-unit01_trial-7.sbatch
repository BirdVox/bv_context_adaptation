#!/bin/bash

#BATCH --job-name=045_aug-all_test-unit01_predict-unit01_trial-7
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:30:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/slurm_045_aug-all_test-unit01_predict-unit01_trial-7_%j.out

module purge

# The first argument is the kind of data augmentation.
# The second argument is the test unit.
# The third argument is the prediction unit.
# The fourth argument is the trial index.
python ../../../src/045_evaluate-add-convnet-full-audio.py all unit01 unit01 7