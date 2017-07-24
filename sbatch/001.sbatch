#!/bin/bash

#BATCH --job-name=001
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:30:00
#SBATCH --mem=1GB
#SBATCH --output=slurm_001_%j.out

module purge

python ../src/001_generate_BirdVox-70k_jams.py
