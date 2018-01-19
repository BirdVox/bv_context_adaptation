# This shell script executes Slurm jobs for thresholding
# predictions of convolutional
# neural network with adaptive threshold on BirdVox-70k full audio
# with logmelspec input.
# Augmentation kind: all.
# Test unit: unit05.
# Trial ID: 0.

sbatch 045_aug-all_test-unit05_predict-unit05_trial-0.sbatch
sbatch 045_aug-all_test-unit05_predict-unit02_trial-0.sbatch
sbatch 045_aug-all_test-unit05_predict-unit03_trial-0.sbatch
