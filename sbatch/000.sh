# This shell script executes all 6 Slurm jobs for generating the BirdVox-70k
# dataset. Every job corresponds to a different recording unit.

sbatch 000-01.sbatch
sbatch 000-02.sbatch
sbatch 000-03.sbatch
sbatch 000-05.sbatch
sbatch 000-07.sbatch
sbatch 000-10.sbatch
