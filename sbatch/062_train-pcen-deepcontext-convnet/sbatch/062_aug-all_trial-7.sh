# This shell script executes Slurm jobs for training
# deep context-adaptive convolutional neural networks
# on BirdVox-70k with PCEN input.
# Trial ID: 7.
# Augmentation kind: all.

sbatch 062_aug-all_unit01_trial-7.sbatch
sbatch 062_aug-all_unit02_trial-7.sbatch
sbatch 062_aug-all_unit03_trial-7.sbatch
sbatch 062_aug-all_unit05_trial-7.sbatch
sbatch 062_aug-all_unit07_trial-7.sbatch
sbatch 062_aug-all_unit10_trial-7.sbatch
