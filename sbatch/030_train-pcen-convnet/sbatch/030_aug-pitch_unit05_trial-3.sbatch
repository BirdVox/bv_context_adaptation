#!/bin/bash

#BATCH --job-name=030_aug-pitch_unit05_trial-3
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=48:00:00
#SBATCH --mem=4GB
#SBATCH --gres=gpu:1
#SBATCH --output=../slurm/slurm_030_aug-pitch_unit05_trial-3_%j.out

module purge
module load cuda/8.0.44
module load cudnn/8.0v5.1

# The first argument is the kind of augmentation.
# The second argument is the name of the recording unit.
# The third argument is name of trial.
python ../../../src/030_train-pcen-convnet.py pitch unit05 trial-3