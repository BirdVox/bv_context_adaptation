# This shell script executes Slurm jobs for training
# context-aware convolutional neural network (adaptive bias)
# on BirdVox-70k.
# Trial ID: 4.
# Augmentation kind: none.

sbatch 037_aug-none_unit01_trial-4.sbatch
sbatch 037_aug-none_unit02_trial-4.sbatch
sbatch 037_aug-none_unit03_trial-4.sbatch
sbatch 037_aug-none_unit05_trial-4.sbatch
sbatch 037_aug-none_unit07_trial-4.sbatch
sbatch 037_aug-none_unit10_trial-4.sbatch
