#!/bin/bash

#BATCH --job-name=060_unit01
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=2:00:00
#SBATCH --mem=4GB
#SBATCH --output=../slurm/slurm_060_unit01_%j.out

module purge

# The argument is the name of the recording unit.
python ../../../src/060_compute-full-birdpcen.py unit01