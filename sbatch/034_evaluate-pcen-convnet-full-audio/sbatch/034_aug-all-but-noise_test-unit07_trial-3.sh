# This shell script executes Slurm jobs for thresholding
# Justin Salamon's ICASSP 2017 predictions of convolutional
# neural network on BirdVox-70k full audio
# with PCEN input.
# Augmentation kind: all-but-noise.
# Test unit: unit07.
# Trial ID: 3.

sbatch 034_aug-all-but-noise_test-unit07_predict-unit07_trial-3.sbatch
sbatch 034_aug-all-but-noise_test-unit07_predict-unit03_trial-3.sbatch
sbatch 034_aug-all-but-noise_test-unit07_predict-unit05_trial-3.sbatch
