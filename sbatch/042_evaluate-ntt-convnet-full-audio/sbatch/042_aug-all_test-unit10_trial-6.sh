# This shell script executes Slurm jobs for thresholding
# predictions of NTT-like convolutional
# neural network on BirdVox-70k full audio
# with logmelspec input.
# Augmentation kind: all.
# Test unit: unit10.
# Trial ID: 6.

sbatch 042_aug-all_test-unit10_predict-unit10_trial-6.sbatch
sbatch 042_aug-all_test-unit10_predict-unit05_trial-6.sbatch
sbatch 042_aug-all_test-unit10_predict-unit07_trial-6.sbatch
