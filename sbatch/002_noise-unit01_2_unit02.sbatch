#!/bin/bash

#BATCH --job-name=002_noise-unit01_2_unit02
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=2:00:00
#SBATCH --mem=4GB
#SBATCH --output=slurm_002_noise-unit01_2_unit02_%j.out

module purge

python ../src/002_augment_BirdVox-70k.py noise-unit01 2 02