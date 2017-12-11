#!/bin/bash

#BATCH --job-name=034_aug-none_test-unit01_predict-unit07_trial-8_th-140
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/slurm_034_aug-none_test-unit01_predict-unit07_trial-8_th-140_%j.out

module purge

# The first argument is the kind of data augmentation.
# The second argument is the test unit.
# The third argument is the prediction unit.
# The fourth argument is the trial index.
# The fifth argument is the threshold range.
python ../../../src/034_evaluate-pcen-convnet-full-audio.py none unit01 unit07 8 140