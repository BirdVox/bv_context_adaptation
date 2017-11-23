# This shell script executes Slurm jobs for training
# Justin Salamon's ICASSP 2017 convolutional neural network
# on BirdVox-70k with PCEN input instead of
# log-mel-spectrogram (logmelspec) input.
# Trial ID: 6.
# Augmentation kind: stretch.

sbatch 030_aug-stretch_unit01_trial-6.sbatch
sbatch 030_aug-stretch_unit02_trial-6.sbatch
sbatch 030_aug-stretch_unit03_trial-6.sbatch
sbatch 030_aug-stretch_unit05_trial-6.sbatch
sbatch 030_aug-stretch_unit07_trial-6.sbatch
sbatch 030_aug-stretch_unit10_trial-6.sbatch
