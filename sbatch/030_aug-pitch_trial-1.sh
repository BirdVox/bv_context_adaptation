# This shell script executes Slurm jobs for training
# Justin Salamon's ICASSP 2017 convolutional neural network
# on BirdVox-70k with PCEN input instead of
# log-mel-spectrogram (logmelspec) input.
# Trial ID: 1.
# Augmentation kind: pitch.

sbatch 030_aug-pitch_unit01_trial-1.sbatch
sbatch 030_aug-pitch_unit02_trial-1.sbatch
sbatch 030_aug-pitch_unit03_trial-1.sbatch
sbatch 030_aug-pitch_unit05_trial-1.sbatch
sbatch 030_aug-pitch_unit07_trial-1.sbatch
sbatch 030_aug-pitch_unit10_trial-1.sbatch
