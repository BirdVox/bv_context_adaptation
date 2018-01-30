# This shell script executes Slurm jobs for running predictions
# with NTT-like convolutional neural network
# on BirdVox-70k, full audio, with PCEN input.
# Trial ID: 4.
# Augmentation kind: none.

sbatch 049_aug-none_test-unit01_trial-4_predict-unit07.sbatch
sbatch 049_aug-none_test-unit01_trial-4_predict-unit10.sbatch
sbatch 049_aug-none_test-unit01_trial-4_predict-unit01.sbatch

sbatch 049_aug-none_test-unit02_trial-4_predict-unit10.sbatch
sbatch 049_aug-none_test-unit02_trial-4_predict-unit01.sbatch
sbatch 049_aug-none_test-unit02_trial-4_predict-unit02.sbatch

sbatch 049_aug-none_test-unit03_trial-4_predict-unit01.sbatch
sbatch 049_aug-none_test-unit03_trial-4_predict-unit02.sbatch
sbatch 049_aug-none_test-unit03_trial-4_predict-unit03.sbatch

sbatch 049_aug-none_test-unit05_trial-4_predict-unit02.sbatch
sbatch 049_aug-none_test-unit05_trial-4_predict-unit03.sbatch
sbatch 049_aug-none_test-unit05_trial-4_predict-unit05.sbatch

sbatch 049_aug-none_test-unit07_trial-4_predict-unit03.sbatch
sbatch 049_aug-none_test-unit07_trial-4_predict-unit05.sbatch
sbatch 049_aug-none_test-unit07_trial-4_predict-unit07.sbatch

sbatch 049_aug-none_test-unit10_trial-4_predict-unit05.sbatch
sbatch 049_aug-none_test-unit10_trial-4_predict-unit07.sbatch
sbatch 049_aug-none_test-unit10_trial-4_predict-unit10.sbatch

