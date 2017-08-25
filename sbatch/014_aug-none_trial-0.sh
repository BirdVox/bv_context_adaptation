# This shell script executes Slurm jobs for running predictions
# with Justin Salamon's ICASSP 2017 convolutional neural network
# on BirdVox-70k.
# Trial ID: 0.
# Augmentation kind: none.

sbatch 014_aug-none_test-unit01_trial-0_predict-unit07.sbatch
sbatch 014_aug-none_test-unit01_trial-0_predict-unit10.sbatch
sbatch 014_aug-none_test-unit01_trial-0_predict-unit01.sbatch

sbatch 014_aug-none_test-unit02_trial-0_predict-unit10.sbatch
sbatch 014_aug-none_test-unit02_trial-0_predict-unit01.sbatch
sbatch 014_aug-none_test-unit02_trial-0_predict-unit02.sbatch

sbatch 014_aug-none_test-unit03_trial-0_predict-unit01.sbatch
sbatch 014_aug-none_test-unit03_trial-0_predict-unit02.sbatch
sbatch 014_aug-none_test-unit03_trial-0_predict-unit03.sbatch

sbatch 014_aug-none_test-unit05_trial-0_predict-unit02.sbatch
sbatch 014_aug-none_test-unit05_trial-0_predict-unit03.sbatch
sbatch 014_aug-none_test-unit05_trial-0_predict-unit05.sbatch

sbatch 014_aug-none_test-unit07_trial-0_predict-unit03.sbatch
sbatch 014_aug-none_test-unit07_trial-0_predict-unit05.sbatch
sbatch 014_aug-none_test-unit07_trial-0_predict-unit07.sbatch

sbatch 014_aug-none_test-unit10_trial-0_predict-unit05.sbatch
sbatch 014_aug-none_test-unit10_trial-0_predict-unit07.sbatch
sbatch 014_aug-none_test-unit10_trial-0_predict-unit10.sbatch

