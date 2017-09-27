#!/bin/bash

#BATCH --job-name=015_aug-noise_test-unit03_trial-8_predict-unit03
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=16:00:00
#SBATCH --mem=250MB
#SBATCH --output=../slurm/015_aug-noise_test-unit03_trial-8_predict-unit03_%j.out

module purge
module load cuda/8.0.44
module load cudnn/8.0v5.1

# The first argument is the kind of augmentation.
# The second argument is the name of the test unit.
# The third argument is name of trial.
# The fourth argument is the name of the prediction unit.
python ../../../src/015_predict-icassp-convnet-full-audio.py noise unit03 trial-8 unit03