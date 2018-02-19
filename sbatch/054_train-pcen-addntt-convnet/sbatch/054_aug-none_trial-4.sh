# This shell script executes Slurm jobs for training
# add-NTT convolutional neural network
# on BirdVox-70k with PCEN input.
# Trial ID: 4.
# Augmentation kind: none.

sbatch 054_aug-none_unit01_trial-4.sbatch
sbatch 054_aug-none_unit02_trial-4.sbatch
sbatch 054_aug-none_unit03_trial-4.sbatch
sbatch 054_aug-none_unit05_trial-4.sbatch
sbatch 054_aug-none_unit07_trial-4.sbatch
sbatch 054_aug-none_unit10_trial-4.sbatch
