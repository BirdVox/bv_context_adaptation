# This shell script executes Slurm jobs for running predictions
# with NTT-like convolutional neural network
# on BirdVox-70k with PCEN input.
# Trial ID: 3.
# Augmentation kind: none.

sbatch 047_aug-none_test-unit01_trial-3_predict-unit07.sbatch
sbatch 047_aug-none_test-unit01_trial-3_predict-unit10.sbatch
sbatch 047_aug-none_test-unit01_trial-3_predict-unit01.sbatch

sbatch 047_aug-none_test-unit02_trial-3_predict-unit10.sbatch
sbatch 047_aug-none_test-unit02_trial-3_predict-unit01.sbatch
sbatch 047_aug-none_test-unit02_trial-3_predict-unit02.sbatch

sbatch 047_aug-none_test-unit03_trial-3_predict-unit01.sbatch
sbatch 047_aug-none_test-unit03_trial-3_predict-unit02.sbatch
sbatch 047_aug-none_test-unit03_trial-3_predict-unit03.sbatch

sbatch 047_aug-none_test-unit05_trial-3_predict-unit02.sbatch
sbatch 047_aug-none_test-unit05_trial-3_predict-unit03.sbatch
sbatch 047_aug-none_test-unit05_trial-3_predict-unit05.sbatch

sbatch 047_aug-none_test-unit07_trial-3_predict-unit03.sbatch
sbatch 047_aug-none_test-unit07_trial-3_predict-unit05.sbatch
sbatch 047_aug-none_test-unit07_trial-3_predict-unit07.sbatch

sbatch 047_aug-none_test-unit10_trial-3_predict-unit05.sbatch
sbatch 047_aug-none_test-unit10_trial-3_predict-unit07.sbatch
sbatch 047_aug-none_test-unit10_trial-3_predict-unit10.sbatch

