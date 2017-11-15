#!/bin/bash

#BATCH --job-name=026_T-0002_unit03
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=8:00:00
#SBATCH --mem=8GB
#SBATCH --output=../slurm/slurm_026_T-0002_unit03_%j.out

module purge

# The first argument is the name of the recording unit.
# The second argument is the duration of background.
python ../../../src/026_compute-clip-background-summaries.py 0002 unit03