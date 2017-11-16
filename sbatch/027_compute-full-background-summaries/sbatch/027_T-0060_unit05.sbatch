#!/bin/bash

#BATCH --job-name=027_T-0060_unit05
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=8:00:00
#SBATCH --mem=8GB
#SBATCH --output=../slurm/slurm_027_T-0060_unit05_%j.out

module purge

# The first argument is the name of the recording unit.
# The second argument is the duration of background.
python ../../../src/027_compute-full-background-summaries.py 0060 unit05