#!/bin/bash

#BATCH --job-name=008_unit07_thrush_50:54
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=4:00:00
#SBATCH --mem=1GB
#SBATCH --output=slurm_008_unit07_thrush_50:54_%j.out

module purge

# The first argument is the name of the recording unit.
# The second argument is the kind of onset detection function.
# The third argument is the range of threshold IDs.
python ../src/008_threshold-oldbird.py unit07 thrush 50:54