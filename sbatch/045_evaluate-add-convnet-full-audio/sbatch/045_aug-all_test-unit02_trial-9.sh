# This shell script executes Slurm jobs for thresholding
# predictions of convolutional
# neural network with adaptive threshold on BirdVox-70k full audio
# with logmelspec input.
# Augmentation kind: all.
# Test unit: unit02.
# Trial ID: 9.

sbatch 045_aug-all_test-unit02_predict-unit02_trial-9.sbatch
sbatch 045_aug-all_test-unit02_predict-unit10_trial-9.sbatch
sbatch 045_aug-all_test-unit02_predict-unit01_trial-9.sbatch
