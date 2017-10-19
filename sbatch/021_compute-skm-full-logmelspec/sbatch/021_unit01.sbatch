#!/bin/bash

#BATCH --job-name=021_unit01
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=2:00:00
#SBATCH --mem=4GB
#SBATCH --output=../slurm/slurm_021_unit01_%j.out

module purge

# The argument is the name of the recording unit.
python ../../../src/021_compute-skm-full-logmelspec.py unit01