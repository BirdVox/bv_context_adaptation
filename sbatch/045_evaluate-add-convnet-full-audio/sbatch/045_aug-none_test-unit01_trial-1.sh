# This shell script executes Slurm jobs for thresholding
# predictions of convolutional
# neural network with adaptive threshold on BirdVox-70k full audio
# with logmelspec input.
# Augmentation kind: none.
# Test unit: unit01.
# Trial ID: 1.

sbatch 045_aug-none_test-unit01_predict-unit01_trial-1.sbatch
sbatch 045_aug-none_test-unit01_predict-unit07_trial-1.sbatch
sbatch 045_aug-none_test-unit01_predict-unit10_trial-1.sbatch
