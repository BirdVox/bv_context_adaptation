#!/bin/bash

#BATCH --job-name=041b_T-0300_unit07
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:15:00
#SBATCH --mem=8GB
#SBATCH --output=../slurm/slurm_041b_T-0300_unit07_%j.out

module purge

# The first argument is the name of the recording unit.
# The second argument is the duration of background.
python ../../../src/041b_compute-pcen-full-background-summaries.py 0300 unit07