# This shell script executes Slurm jobs for training
# add-NTT convolutional neural network
# on BirdVox-70k with PCEN input.
# Trial ID: 4.
# Augmentation kind: all-but-noise.

sbatch 054_aug-all-but-noise_unit01_trial-4.sbatch
sbatch 054_aug-all-but-noise_unit02_trial-4.sbatch
sbatch 054_aug-all-but-noise_unit03_trial-4.sbatch
sbatch 054_aug-all-but-noise_unit05_trial-4.sbatch
sbatch 054_aug-all-but-noise_unit07_trial-4.sbatch
sbatch 054_aug-all-but-noise_unit10_trial-4.sbatch
