#!/bin/bash

#BATCH --job-name=010
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:10:00
#SBATCH --mem=16GB
#SBATCH --output=slurm_010_%j.out

module purge

python ../src/010_merge-tseep-thrush.py
