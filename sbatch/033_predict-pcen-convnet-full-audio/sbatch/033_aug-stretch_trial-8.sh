# This shell script executes Slurm jobs for running predictions
# with Justin Salamon's ICASSP 2017 convolutional neural network
# on BirdVox-70k, full audio, with PCEN input.
# Trial ID: 8.
# Augmentation kind: stretch.

sbatch 033_aug-stretch_test-unit01_trial-8_predict-unit07.sbatch
sbatch 033_aug-stretch_test-unit01_trial-8_predict-unit10.sbatch
sbatch 033_aug-stretch_test-unit01_trial-8_predict-unit01.sbatch

sbatch 033_aug-stretch_test-unit02_trial-8_predict-unit10.sbatch
sbatch 033_aug-stretch_test-unit02_trial-8_predict-unit01.sbatch
sbatch 033_aug-stretch_test-unit02_trial-8_predict-unit02.sbatch

sbatch 033_aug-stretch_test-unit03_trial-8_predict-unit01.sbatch
sbatch 033_aug-stretch_test-unit03_trial-8_predict-unit02.sbatch
sbatch 033_aug-stretch_test-unit03_trial-8_predict-unit03.sbatch

sbatch 033_aug-stretch_test-unit05_trial-8_predict-unit02.sbatch
sbatch 033_aug-stretch_test-unit05_trial-8_predict-unit03.sbatch
sbatch 033_aug-stretch_test-unit05_trial-8_predict-unit05.sbatch

sbatch 033_aug-stretch_test-unit07_trial-8_predict-unit03.sbatch
sbatch 033_aug-stretch_test-unit07_trial-8_predict-unit05.sbatch
sbatch 033_aug-stretch_test-unit07_trial-8_predict-unit07.sbatch

sbatch 033_aug-stretch_test-unit10_trial-8_predict-unit05.sbatch
sbatch 033_aug-stretch_test-unit10_trial-8_predict-unit07.sbatch
sbatch 033_aug-stretch_test-unit10_trial-8_predict-unit10.sbatch

