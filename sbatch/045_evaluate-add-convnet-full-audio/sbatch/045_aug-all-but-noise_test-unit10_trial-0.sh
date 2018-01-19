# This shell script executes Slurm jobs for thresholding
# predictions of convolutional
# neural network with adaptive threshold on BirdVox-70k full audio
# with logmelspec input.
# Augmentation kind: all-but-noise.
# Test unit: unit10.
# Trial ID: 0.

sbatch 045_aug-all-but-noise_test-unit10_predict-unit10_trial-0.sbatch
sbatch 045_aug-all-but-noise_test-unit10_predict-unit05_trial-0.sbatch
sbatch 045_aug-all-but-noise_test-unit10_predict-unit07_trial-0.sbatch
