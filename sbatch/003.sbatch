#!/bin/bash

#BATCH --job-name=003
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=2:00:00
#SBATCH --mem=32GB
#SBATCH --output=slurm_003_%j.out

module purge

python ../src/003_save-hdf5.py
