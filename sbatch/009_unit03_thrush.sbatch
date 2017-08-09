#!/bin/bash

#BATCH --job-name=009_unit03_thrush
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:30:00
#SBATCH --mem=1GB
#SBATCH --output=slurm_009_unit03_thrush_%j.out

module purge

# The first argument is the name of the recording unit.
# The second argument is the kind of onset detection function.
python ../src/009_suppress-clips-oldbird.py unit03 thrush