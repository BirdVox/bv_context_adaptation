# This shell script executes Slurm jobs for thresholding
# predictions of NTT-like convolutional
# neural network on BirdVox-70k full audio
# with logmelspec input.
# Augmentation kind: none.
# Test unit: unit01.
# Trial ID: 4.

sbatch 042_aug-none_test-unit01_predict-unit01_trial-4.sbatch
sbatch 042_aug-none_test-unit01_predict-unit07_trial-4.sbatch
sbatch 042_aug-none_test-unit01_predict-unit10_trial-4.sbatch
