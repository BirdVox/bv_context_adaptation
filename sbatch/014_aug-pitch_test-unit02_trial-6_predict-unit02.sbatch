#!/bin/bash

#BATCH --job-name=014_aug-pitch_test-unit02_trial-6_predict-unit02
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:10:00
#SBATCH --mem=100MB
#SBATCH --output=slurm_014_aug-pitch_test-unit02_trial-6_predict-unit02_%j.out

module purge
module load cuda/8.0.44
module load cudnn/8.0v5.1

# The first argument is the kind of augmentation.
# The second argument is the name of the test unit.
# The third argument is name of trial.
# The fourth argument is the name of the prediction unit.
python ../src/014_predict-icassp-convnet.py pitch unit02 trial-6 unit02