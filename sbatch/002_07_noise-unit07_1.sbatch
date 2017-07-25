#!/bin/bash

#BATCH --job-name=002_07_noise-unit07_1
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=2:00:00
#SBATCH --mem=4GB
#SBATCH --output=slurm_002_07_noise-unit07_1_%j.out

module purge

python ../src/002_augment_BirdVox-70k.py 07 noise-unit07 1