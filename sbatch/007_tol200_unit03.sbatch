#!/bin/bash

#BATCH --job-name=007_tol200_unit03
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=4:00:00
#SBATCH --mem=16GB
#SBATCH --output=slurm_007_tol200_unit03_%j.out

module purge

# The first argument is the tolerance in milliseconds.
# The second argument is the name of the recording unit.
python ../src/007_evaluate-skm.py 200 unit03