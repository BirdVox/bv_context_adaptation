# This shell script executes Slurm jobs for thresholding
# Justin Salamon's ICASSP 2017 predictions of convolutional
# neural network on BirdVox-70k full audio
# with PCEN input.
# Augmentation kind: none.
# Test unit: unit03.
# Trial ID: 6.

sbatch 034_aug-none_test-unit03_predict-unit03_trial-6.sbatch
sbatch 034_aug-none_test-unit03_predict-unit01_trial-6.sbatch
sbatch 034_aug-none_test-unit03_predict-unit02_trial-6.sbatch
