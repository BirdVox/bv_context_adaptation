# This shell script executes the Slurm jobs for data augmentation.

sbatch 002-01-noise.sbatch
sbatch 002-01-original.sbatch
sbatch 002-01-pitch.sbatch
sbatch 002-01-stretch.sbatch

sbatch 002-02-noise.sbatch
sbatch 002-02-original.sbatch
sbatch 002-02-pitch.sbatch
sbatch 002-02-stretch.sbatch

sbatch 002-03-noise.sbatch
sbatch 002-03-original.sbatch
sbatch 002-03-pitch.sbatch
sbatch 002-03-stretch.sbatch

sbatch 002-05-noise.sbatch
sbatch 002-05-original.sbatch
sbatch 002-05-pitch.sbatch
sbatch 002-05-stretch.sbatch

sbatch 002-07-noise.sbatch
sbatch 002-07-original.sbatch
sbatch 002-07-pitch.sbatch
sbatch 002-07-stretch.sbatch

sbatch 002-10-noise.sbatch
sbatch 002-10-original.sbatch
sbatch 002-10-pitch.sbatch
sbatch 002-10-stretch.sbatch


