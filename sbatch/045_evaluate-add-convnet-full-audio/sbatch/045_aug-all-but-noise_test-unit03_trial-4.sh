# This shell script executes Slurm jobs for thresholding
# predictions of convolutional
# neural network with adaptive threshold on BirdVox-70k full audio
# with logmelspec input.
# Augmentation kind: all-but-noise.
# Test unit: unit03.
# Trial ID: 4.

sbatch 045_aug-all-but-noise_test-unit03_predict-unit03_trial-4.sbatch
sbatch 045_aug-all-but-noise_test-unit03_predict-unit01_trial-4.sbatch
sbatch 045_aug-all-but-noise_test-unit03_predict-unit02_trial-4.sbatch
