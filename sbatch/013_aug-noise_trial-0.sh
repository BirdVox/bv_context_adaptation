# This shell script executes Slurm jobs for training
# Justin Salamon's ICASSP 2017 convolutional neural network
# on BirdVox-70k.
# Trial ID: 0.
# Augmentation kind: noise.

sbatch 013_aug-noise_unit01_trial-0.sbatch
sbatch 013_aug-noise_unit02_trial-0.sbatch
sbatch 013_aug-noise_unit03_trial-0.sbatch
sbatch 013_aug-noise_unit05_trial-0.sbatch
sbatch 013_aug-noise_unit07_trial-0.sbatch
sbatch 013_aug-noise_unit10_trial-0.sbatch