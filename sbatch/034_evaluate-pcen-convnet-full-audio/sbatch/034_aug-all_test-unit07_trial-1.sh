# This shell script executes Slurm jobs for thresholding
# Justin Salamon's ICASSP 2017 predictions of convolutional
# neural network on BirdVox-70k full audio
# with PCEN input.
# Augmentation kind: all.
# Test unit: unit07.
# Trial ID: 1.

sbatch 034_aug-all_test-unit07_predict-unit07_trial-1.sbatch
sbatch 034_aug-all_test-unit07_predict-unit03_trial-1.sbatch
sbatch 034_aug-all_test-unit07_predict-unit05_trial-1.sbatch
