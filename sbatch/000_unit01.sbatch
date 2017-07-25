#!/bin/bash

#BATCH --job-name=000_unit01
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:30:00
#SBATCH --mem=4GB
#SBATCH --output=slurm_000_unit01_%j.out

module purge

# The integer passed to the Python script 000_generate-wav.py
# corresponds to the ID of the recording unit.
python ../src/000_generate-wav.py 01