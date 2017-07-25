#!/bin/bash

#BATCH --job-name=002_01_noise-unit05_0
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=2:00:00
#SBATCH --mem=4GB
#SBATCH --output=slurm_002_01_noise-unit05_0_%j.out

module purge

python ../src/002_augment_BirdVox-70k.py 01 noise-unit05 0