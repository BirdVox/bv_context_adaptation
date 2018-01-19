# This shell script executes Slurm jobs for thresholding
# predictions of convolutional
# neural network with adaptive threshold on BirdVox-70k full audio
# with logmelspec input.
# Augmentation kind: all.
# Test unit: unit07.
# Trial ID: 3.

sbatch 045_aug-all_test-unit07_predict-unit07_trial-3.sbatch
sbatch 045_aug-all_test-unit07_predict-unit03_trial-3.sbatch
sbatch 045_aug-all_test-unit07_predict-unit05_trial-3.sbatch
