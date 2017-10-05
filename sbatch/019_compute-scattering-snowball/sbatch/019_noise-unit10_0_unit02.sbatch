#!/bin/bash

#BATCH --job-name=019_noise-unit10_0_unit02
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=12:00:00
#SBATCH --mem=1GB
#SBATCH --output=../slurm/slurm_019_noise-unit10_0_unit02_%j.out

module purge
module load matlab/2017a

# The first argument is the name of the augmentation.
# The second argument is the instance ID of the augmentation.
# The third argument is the name of the recording unit.
python ../../../src/019_compute-scattering-snowball.py noise-unit10 0 unit02