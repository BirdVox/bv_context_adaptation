#!/bin/bash

#BATCH --job-name=026_T-7200_unit01
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=8:00:00
#SBATCH --mem=8GB
#SBATCH --output=../slurm/slurm_026_T-7200_unit01_%j.out

module purge

# The first argument is the name of the recording unit.
# The second argument is the duration of background.
python ../../../src/026_compute-clip-background-summaries.py 7200 unit01