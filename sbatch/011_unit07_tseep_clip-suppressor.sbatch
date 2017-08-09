#!/bin/bash

#BATCH --job-name=011_unit07_tseep_clip-suppressor
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=1:00:00
#SBATCH --mem=1GB
#SBATCH --output=slurm_011_unit07_tseep_clip-suppressor_%j.out

module purge

# The first argument is the name of the recording unit.
# The second argument is the kind of onset detection function.
# The third argument triggers the clip suppressor.
python ../src/011_evaluate-oldbird-per-unit.py unit07 tseep clip-suppressor