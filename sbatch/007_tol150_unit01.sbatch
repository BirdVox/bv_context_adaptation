#!/bin/bash

#BATCH --job-name=007_tol150_unit01
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=1:00:00
#SBATCH --mem=4GB
#SBATCH --output=slurm_007_tol150_unit01_%j.out

module purge

# The first argument is the tolerance in milliseconds.
# The second argument is the name of the recording unit.
python ../src/007_evaluate-skm.py 150 unit01