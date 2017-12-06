# This shell script executes Slurm jobs for training
# NTT convolutional neural network
# on BirdVox-70k.
# Trial ID: 2.
# Augmentation kind: all.

sbatch 035_aug-all_unit01_trial-2.sbatch
sbatch 035_aug-all_unit02_trial-2.sbatch
sbatch 035_aug-all_unit03_trial-2.sbatch
sbatch 035_aug-all_unit05_trial-2.sbatch
sbatch 035_aug-all_unit07_trial-2.sbatch
sbatch 035_aug-all_unit10_trial-2.sbatch
