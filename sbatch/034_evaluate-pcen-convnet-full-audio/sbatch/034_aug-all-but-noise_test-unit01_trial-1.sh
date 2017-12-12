# This shell script executes Slurm jobs for thresholding
# Justin Salamon's ICASSP 2017 predictions of convolutional
# neural network on BirdVox-70k full audio
# with PCEN input.
# Augmentation kind: all-but-noise.
# Test unit: unit01.
# Trial ID: 1.

sbatch 034_aug-all-but-noise_test-unit01_predict-unit01_trial-1.sbatch
sbatch 034_aug-all-but-noise_test-unit01_predict-unit07_trial-1.sbatch
sbatch 034_aug-all-but-noise_test-unit01_predict-unit10_trial-1.sbatch
