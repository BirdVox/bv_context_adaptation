# This shell script executes Slurm jobs for training
# context-aware convolutional neural network (adaptive bias)
# on BirdVox-70k.
# Trial ID: 2.
# Augmentation kind: all.

sbatch 037_aug-all_unit01_trial-2.sbatch
sbatch 037_aug-all_unit02_trial-2.sbatch
sbatch 037_aug-all_unit03_trial-2.sbatch
sbatch 037_aug-all_unit05_trial-2.sbatch
sbatch 037_aug-all_unit07_trial-2.sbatch
sbatch 037_aug-all_unit10_trial-2.sbatch
