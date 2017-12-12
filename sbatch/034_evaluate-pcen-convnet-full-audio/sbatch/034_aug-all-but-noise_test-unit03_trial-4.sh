# This shell script executes Slurm jobs for thresholding
# Justin Salamon's ICASSP 2017 predictions of convolutional
# neural network on BirdVox-70k full audio
# with PCEN input.
# Augmentation kind: all-but-noise.
# Test unit: unit03.
# Trial ID: 4.

sbatch 034_aug-all-but-noise_test-unit03_predict-unit03_trial-4.sbatch
sbatch 034_aug-all-but-noise_test-unit03_predict-unit01_trial-4.sbatch
sbatch 034_aug-all-but-noise_test-unit03_predict-unit02_trial-4.sbatch
