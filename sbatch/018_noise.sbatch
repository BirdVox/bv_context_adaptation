#!/bin/bash

#BATCH --job-name=018_noise
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:10:00
#SBATCH --mem=1GB
#SBATCH --output=slurm_018_noise_%j.out

module purge

# The argument is the kind of data augmentation.
python ../src/018_evaluate-icassp-convnet-clips.py noise