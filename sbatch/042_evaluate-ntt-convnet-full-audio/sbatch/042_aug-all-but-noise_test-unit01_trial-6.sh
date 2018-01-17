# This shell script executes Slurm jobs for thresholding
# predictions of NTT-like convolutional
# neural network on BirdVox-70k full audio
# with logmelspec input.
# Augmentation kind: all-but-noise.
# Test unit: unit01.
# Trial ID: 6.

sbatch 042_aug-all-but-noise_test-unit01_predict-unit01_trial-6.sbatch
sbatch 042_aug-all-but-noise_test-unit01_predict-unit07_trial-6.sbatch
sbatch 042_aug-all-but-noise_test-unit01_predict-unit10_trial-6.sbatch
