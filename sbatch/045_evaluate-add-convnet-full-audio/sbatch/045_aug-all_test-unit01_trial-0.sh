# This shell script executes Slurm jobs for thresholding
# predictions of convolutional
# neural network with adaptive threshold on BirdVox-70k full audio
# with logmelspec input.
# Augmentation kind: all.
# Test unit: unit01.
# Trial ID: 0.

sbatch 045_aug-all_test-unit01_predict-unit01_trial-0.sbatch
sbatch 045_aug-all_test-unit01_predict-unit07_trial-0.sbatch
sbatch 045_aug-all_test-unit01_predict-unit10_trial-0.sbatch
