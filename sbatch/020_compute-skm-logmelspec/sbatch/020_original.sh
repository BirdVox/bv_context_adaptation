# This shell script executes the Slurm jobs for computing log-mel-spectrograms for SKM-SVM model.

sbatch 020_original_unit01.sbatch
sbatch 020_original_unit02.sbatch
sbatch 020_original_unit03.sbatch
sbatch 020_original_unit05.sbatch
sbatch 020_original_unit07.sbatch
sbatch 020_original_unit10.sbatch

