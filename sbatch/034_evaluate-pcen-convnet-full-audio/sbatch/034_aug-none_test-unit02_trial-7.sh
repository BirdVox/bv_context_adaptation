# This shell script executes Slurm jobs for thresholding
# Justin Salamon's ICASSP 2017 predictions of convolutional
# neural network on BirdVox-70k full audio
# with PCEN input.
# Augmentation kind: none.
# Test unit: unit02.
# Trial ID: 7.

sbatch 034_aug-none_test-unit02_predict-unit02_trial-7.sbatch
sbatch 034_aug-none_test-unit02_predict-unit10_trial-7.sbatch
sbatch 034_aug-none_test-unit02_predict-unit01_trial-7.sbatch
