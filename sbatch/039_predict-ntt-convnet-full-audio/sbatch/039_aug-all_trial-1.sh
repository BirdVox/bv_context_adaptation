# This shell script executes Slurm jobs for running predictions
# with NTT-like convolutional neural network
# on BirdVox-70k, full audio.
# Trial ID: 1.
# Augmentation kind: all.

sbatch 039_aug-all_test-unit01_trial-1_predict-unit07.sbatch
sbatch 039_aug-all_test-unit01_trial-1_predict-unit10.sbatch
sbatch 039_aug-all_test-unit01_trial-1_predict-unit01.sbatch

sbatch 039_aug-all_test-unit02_trial-1_predict-unit10.sbatch
sbatch 039_aug-all_test-unit02_trial-1_predict-unit01.sbatch
sbatch 039_aug-all_test-unit02_trial-1_predict-unit02.sbatch

sbatch 039_aug-all_test-unit03_trial-1_predict-unit01.sbatch
sbatch 039_aug-all_test-unit03_trial-1_predict-unit02.sbatch
sbatch 039_aug-all_test-unit03_trial-1_predict-unit03.sbatch

sbatch 039_aug-all_test-unit05_trial-1_predict-unit02.sbatch
sbatch 039_aug-all_test-unit05_trial-1_predict-unit03.sbatch
sbatch 039_aug-all_test-unit05_trial-1_predict-unit05.sbatch

sbatch 039_aug-all_test-unit07_trial-1_predict-unit03.sbatch
sbatch 039_aug-all_test-unit07_trial-1_predict-unit05.sbatch
sbatch 039_aug-all_test-unit07_trial-1_predict-unit07.sbatch

sbatch 039_aug-all_test-unit10_trial-1_predict-unit05.sbatch
sbatch 039_aug-all_test-unit10_trial-1_predict-unit07.sbatch
sbatch 039_aug-all_test-unit10_trial-1_predict-unit10.sbatch

