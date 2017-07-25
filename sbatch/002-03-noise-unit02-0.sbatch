#!/bin/bash

#BATCH --job-name=002-03-noise-unit02-0
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=2:00:00
#SBATCH --mem=4GB
#SBATCH --output=slurm_002-03-noise-unit02-0_%j.out

module purge

python ../src/002_augment_BirdVox-70k.py 03 noise-unit02 0