#!/bin/bash

#BATCH --job-name=000-0
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:30:00
#SBATCH --mem=4GB
#SBATCH --output=slurm_000-0_%j.out

module purge

# The integer passed to the Python script 000_generate_BirdVox-70k_clips.py
# corresponds to the index of the recording unit in the
# list [1, 2, 3, 5, 7, 10]. It ranges between 0 and 5.
cd ../src
python 000_generate_BirdVox-70k_clips.py 0
