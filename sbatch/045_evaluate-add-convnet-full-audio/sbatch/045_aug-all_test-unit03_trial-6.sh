# This shell script executes Slurm jobs for thresholding
# predictions of convolutional
# neural network with adaptive threshold on BirdVox-70k full audio
# with logmelspec input.
# Augmentation kind: all.
# Test unit: unit03.
# Trial ID: 6.

sbatch 045_aug-all_test-unit03_predict-unit03_trial-6.sbatch
sbatch 045_aug-all_test-unit03_predict-unit01_trial-6.sbatch
sbatch 045_aug-all_test-unit03_predict-unit02_trial-6.sbatch
