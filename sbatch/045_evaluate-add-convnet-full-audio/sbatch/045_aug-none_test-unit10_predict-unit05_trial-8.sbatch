#!/bin/bash

#BATCH --job-name=045_aug-none_test-unit10_predict-unit05_trial-8
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/slurm_045_aug-none_test-unit10_predict-unit05_trial-8_%j.out

module purge

# The first argument is the kind of data augmentation.
# The second argument is the test unit.
# The third argument is the prediction unit.
# The fourth argument is the trial index.
python ../../../src/045_evaluate-add-convnet-full-audio.py none unit10 unit05 8