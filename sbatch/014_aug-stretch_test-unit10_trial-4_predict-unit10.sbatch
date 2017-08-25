#!/bin/bash

#BATCH --job-name=014_aug-stretch_test-unit10_trial-4_predict-unit10
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=1:00:00
#SBATCH --mem=1GB
#SBATCH --output=slurm_014_aug-stretch_test-unit10_trial-4_predict-unit10_%j.out

module purge
module load cuda/8.0.44
module load cudnn/8.0v5.1

# The first argument is the kind of augmentation.
# The second argument is the name of the test unit.
# The third argument is name of trial.
# The fourth argument is the name of the prediction unit.
python ../src/014_predict-icassp-convnet.py stretch unit10 trial-4 unit10