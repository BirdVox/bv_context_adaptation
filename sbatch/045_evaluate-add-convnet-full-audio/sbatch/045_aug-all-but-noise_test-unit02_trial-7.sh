# This shell script executes Slurm jobs for thresholding
# predictions of convolutional
# neural network with adaptive threshold on BirdVox-70k full audio
# with logmelspec input.
# Augmentation kind: all-but-noise.
# Test unit: unit02.
# Trial ID: 7.

sbatch 045_aug-all-but-noise_test-unit02_predict-unit02_trial-7.sbatch
sbatch 045_aug-all-but-noise_test-unit02_predict-unit10_trial-7.sbatch
sbatch 045_aug-all-but-noise_test-unit02_predict-unit01_trial-7.sbatch
