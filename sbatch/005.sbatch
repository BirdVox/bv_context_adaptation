#!/bin/bash

#BATCH --job-name=004
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=1:00:00
#SBATCH --mem=1GB
#SBATCH --output=slurm_004_%j.out

module purge

python ../src/004_archive.py
