#!/bin/bash

#BATCH --job-name=014_aug-none_test-unit01_trial-8_predict-unit07
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:10:00
#SBATCH --mem=500MB
#SBATCH --output=../slurm/slurm_014_aug-none_test-unit01_trial-8_predict-unit07_%j.out

module purge
module load cuda/8.0.44
module load cudnn/8.0v5.1

# The first argument is the kind of augmentation.
# The second argument is the name of the test unit.
# The third argument is name of trial.
# The fourth argument is the name of the prediction unit.
python ../../../src/014_predict-icassp-convnet-clips.py none unit01 trial-8 unit07