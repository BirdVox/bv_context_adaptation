# This shell script executes Slurm jobs for thresholding
# Justin Salamon's ICASSP 2017 predictions of convolutional
# neural network on BirdVox-70k full audio
# with PCEN input.
# Augmentation kind: all.
# Test unit: unit01.
# Trial ID: 5.

sbatch 034_aug-all_test-unit01_predict-unit01_trial-5.sbatch
sbatch 034_aug-all_test-unit01_predict-unit07_trial-5.sbatch
sbatch 034_aug-all_test-unit01_predict-unit10_trial-5.sbatch
