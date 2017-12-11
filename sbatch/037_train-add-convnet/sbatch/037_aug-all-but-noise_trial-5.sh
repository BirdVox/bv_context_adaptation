# This shell script executes Slurm jobs for training
# context-aware convolutional neural network (adaptive bias)
# on BirdVox-70k.
# Trial ID: 5.
# Augmentation kind: all-but-noise.

sbatch 037_aug-all-but-noise_unit01_trial-5.sbatch
sbatch 037_aug-all-but-noise_unit02_trial-5.sbatch
sbatch 037_aug-all-but-noise_unit03_trial-5.sbatch
sbatch 037_aug-all-but-noise_unit05_trial-5.sbatch
sbatch 037_aug-all-but-noise_unit07_trial-5.sbatch
sbatch 037_aug-all-but-noise_unit10_trial-5.sbatch