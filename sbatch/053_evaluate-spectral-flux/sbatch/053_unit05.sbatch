#!/bin/bash

#BATCH --job-name=053_unit05
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:10:00
#SBATCH --mem=1GB
#SBATCH --output=slurm_053_unit05_%j.out

module purge

# The argument is the name of the recording unit.
python ../../../src/053_evaluate-spectral-flux.py unit05