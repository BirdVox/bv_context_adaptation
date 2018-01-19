# This shell script executes Slurm jobs for thresholding
# predictions of convolutional
# neural network with adaptive threshold on BirdVox-70k full audio
# with logmelspec input.
# Augmentation kind: none.
# Test unit: unit10.
# Trial ID: 8.

sbatch 045_aug-none_test-unit10_predict-unit10_trial-8.sbatch
sbatch 045_aug-none_test-unit10_predict-unit05_trial-8.sbatch
sbatch 045_aug-none_test-unit10_predict-unit07_trial-8.sbatch
