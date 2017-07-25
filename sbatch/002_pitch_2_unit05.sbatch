#!/bin/bash

#BATCH --job-name=002_pitch_2_unit05
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=2:00:00
#SBATCH --mem=4GB
#SBATCH --output=slurm_002_pitch_2_unit05_%j.out

module purge

python ../src/002_augment_BirdVox-70k.py pitch 2 05