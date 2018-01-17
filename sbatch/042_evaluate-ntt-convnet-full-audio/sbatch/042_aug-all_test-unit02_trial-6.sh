# This shell script executes Slurm jobs for thresholding
# predictions of NTT-like convolutional
# neural network on BirdVox-70k full audio
# with logmelspec input.
# Augmentation kind: all.
# Test unit: unit02.
# Trial ID: 6.

sbatch 042_aug-all_test-unit02_predict-unit02_trial-6.sbatch
sbatch 042_aug-all_test-unit02_predict-unit10_trial-6.sbatch
sbatch 042_aug-all_test-unit02_predict-unit01_trial-6.sbatch
