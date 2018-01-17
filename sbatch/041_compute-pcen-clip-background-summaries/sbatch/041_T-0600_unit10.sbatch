#!/bin/bash

#BATCH --job-name=041_T-0600_unit10
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=96:00:00
#SBATCH --mem=8GB
#SBATCH --output=../slurm/slurm_041_T-0600_unit10_%j.out

module purge

# The first argument is the name of the recording unit.
# The second argument is the duration of background.
python ../../../src/041_compute-pcen-clip-background-summaries.py 0600 unit10