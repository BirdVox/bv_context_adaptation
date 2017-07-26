#!/bin/bash

#BATCH --job-name=001_unit02
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:30:00
#SBATCH --mem=4GB
#SBATCH --output=slurm_001_unit02_%j.out

module purge

# The argument is the name of the recording unit.
python ../src/001_generate-wav.py unit02