# This shell script executes Slurm jobs for thresholding
# predictions of NTT-like convolutional
# neural network on BirdVox-70k full audio
# with logmelspec input.
# Augmentation kind: all-but-noise.
# Test unit: unit02.
# Trial ID: 8.

sbatch 042_aug-all-but-noise_test-unit02_predict-unit02_trial-8.sbatch
sbatch 042_aug-all-but-noise_test-unit02_predict-unit10_trial-8.sbatch
sbatch 042_aug-all-but-noise_test-unit02_predict-unit01_trial-8.sbatch
