# This shell script executes Slurm jobs for thresholding
# Justin Salamon's ICASSP 2017 predictions of convolutional
# neural network on BirdVox-70k full audio
# with PCEN input.
# Augmentation kind: all.
# Test unit: unit10.
# Trial ID: 0.

sbatch 034_aug-all_test-unit10_predict-unit10_trial-0.sbatch
sbatch 034_aug-all_test-unit10_predict-unit05_trial-0.sbatch
sbatch 034_aug-all_test-unit10_predict-unit07_trial-0.sbatch
