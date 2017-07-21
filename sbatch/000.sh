# This shell script executes all 6 Slurm jobs for generating the BirdVox-70k
# dataset. Every job corresponds to a different recording unit.

sbatch 000-0.sbatch
sbatch 000-1.sbatch
sbatch 000-2.sbatch
sbatch 000-3.sbatch
sbatch 000-4.sbatch
sbatch 000-5.sbatch
