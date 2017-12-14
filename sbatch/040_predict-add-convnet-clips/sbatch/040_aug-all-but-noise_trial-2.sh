# This shell script executes Slurm jobs for running predictions
# with Justin Salamon's ICASSP 2017 convolutional neural network
# on BirdVox-70k.
# Trial ID: 2.
# Augmentation kind: all-but-noise.

sbatch 040_aug-all-but-noise_test-unit01_trial-2_predict-unit07.sbatch
sbatch 040_aug-all-but-noise_test-unit01_trial-2_predict-unit10.sbatch
sbatch 040_aug-all-but-noise_test-unit01_trial-2_predict-unit01.sbatch

sbatch 040_aug-all-but-noise_test-unit02_trial-2_predict-unit10.sbatch
sbatch 040_aug-all-but-noise_test-unit02_trial-2_predict-unit01.sbatch
sbatch 040_aug-all-but-noise_test-unit02_trial-2_predict-unit02.sbatch

sbatch 040_aug-all-but-noise_test-unit03_trial-2_predict-unit01.sbatch
sbatch 040_aug-all-but-noise_test-unit03_trial-2_predict-unit02.sbatch
sbatch 040_aug-all-but-noise_test-unit03_trial-2_predict-unit03.sbatch

sbatch 040_aug-all-but-noise_test-unit05_trial-2_predict-unit02.sbatch
sbatch 040_aug-all-but-noise_test-unit05_trial-2_predict-unit03.sbatch
sbatch 040_aug-all-but-noise_test-unit05_trial-2_predict-unit05.sbatch

sbatch 040_aug-all-but-noise_test-unit07_trial-2_predict-unit03.sbatch
sbatch 040_aug-all-but-noise_test-unit07_trial-2_predict-unit05.sbatch
sbatch 040_aug-all-but-noise_test-unit07_trial-2_predict-unit07.sbatch

sbatch 040_aug-all-but-noise_test-unit10_trial-2_predict-unit05.sbatch
sbatch 040_aug-all-but-noise_test-unit10_trial-2_predict-unit07.sbatch
sbatch 040_aug-all-but-noise_test-unit10_trial-2_predict-unit10.sbatch

