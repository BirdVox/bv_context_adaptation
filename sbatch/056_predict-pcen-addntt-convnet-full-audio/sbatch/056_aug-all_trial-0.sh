# This shell script executes Slurm jobs for running predictions
# with adaptive threshold, mixture-of-experts convolutional neural network
# on BirdVox-70k, full audio, with PCEN input.
# Trial ID: 0.
# Augmentation kind: all.

sbatch 056_aug-all_test-unit01_trial-0_predict-unit07.sbatch
sbatch 056_aug-all_test-unit01_trial-0_predict-unit10.sbatch
sbatch 056_aug-all_test-unit01_trial-0_predict-unit01.sbatch

sbatch 056_aug-all_test-unit02_trial-0_predict-unit10.sbatch
sbatch 056_aug-all_test-unit02_trial-0_predict-unit01.sbatch
sbatch 056_aug-all_test-unit02_trial-0_predict-unit02.sbatch

sbatch 056_aug-all_test-unit03_trial-0_predict-unit01.sbatch
sbatch 056_aug-all_test-unit03_trial-0_predict-unit02.sbatch
sbatch 056_aug-all_test-unit03_trial-0_predict-unit03.sbatch

sbatch 056_aug-all_test-unit05_trial-0_predict-unit02.sbatch
sbatch 056_aug-all_test-unit05_trial-0_predict-unit03.sbatch
sbatch 056_aug-all_test-unit05_trial-0_predict-unit05.sbatch

sbatch 056_aug-all_test-unit07_trial-0_predict-unit03.sbatch
sbatch 056_aug-all_test-unit07_trial-0_predict-unit05.sbatch
sbatch 056_aug-all_test-unit07_trial-0_predict-unit07.sbatch

sbatch 056_aug-all_test-unit10_trial-0_predict-unit05.sbatch
sbatch 056_aug-all_test-unit10_trial-0_predict-unit07.sbatch
sbatch 056_aug-all_test-unit10_trial-0_predict-unit10.sbatch

