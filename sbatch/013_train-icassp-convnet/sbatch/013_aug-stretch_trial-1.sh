# This shell script executes Slurm jobs for training
# Justin Salamon's ICASSP 2017 convolutional neural network
# on BirdVox-70k.
# Trial ID: 1.
# Augmentation kind: stretch.

sbatch 013_aug-stretch_unit01_trial-1.sbatch
sbatch 013_aug-stretch_unit02_trial-1.sbatch
sbatch 013_aug-stretch_unit03_trial-1.sbatch
sbatch 013_aug-stretch_unit05_trial-1.sbatch
sbatch 013_aug-stretch_unit07_trial-1.sbatch
sbatch 013_aug-stretch_unit10_trial-1.sbatch
