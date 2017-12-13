#!/bin/bash

#BATCH --job-name=032_unit02
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=2:00:00
#SBATCH --mem=4GB
#SBATCH --output=../slurm/slurm_032_unit02_%j.out

module purge

# The argument is the name of the recording unit.
python ../../../src/032_compute-full-pcen.py unit02