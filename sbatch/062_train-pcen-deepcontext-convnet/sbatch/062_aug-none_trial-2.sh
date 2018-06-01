# This shell script executes Slurm jobs for training
# deep context-adaptive convolutional neural networks
# on BirdVox-70k with PCEN input.
# Trial ID: 2.
# Augmentation kind: none.

sbatch 062_aug-none_unit01_trial-2.sbatch
sbatch 062_aug-none_unit02_trial-2.sbatch
sbatch 062_aug-none_unit03_trial-2.sbatch
sbatch 062_aug-none_unit05_trial-2.sbatch
sbatch 062_aug-none_unit07_trial-2.sbatch
sbatch 062_aug-none_unit10_trial-2.sbatch
