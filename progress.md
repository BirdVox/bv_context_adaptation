A. Out-of-sample spherical k-means model
1. [DONE] Train on external data.

2. [DONE] Compute predictions on 6 full night recordings.

3. [DONE] Postprocessing: peak-picking, thresholding, event matching.

4. [DONE] Export metrics (n_selected, TP, FP, FN, precision, recall, F)
for all 6 units, 10 tolerances, and 100 thresholds, to 6*10=60 CSV files.

5. [DONE] Compute global metrics (n_selected, TP, FP, FN, precision, recall, F and AUPRC) across all 6 units and 10 tolerances. Store in 1 CSV file.


B. Old Bird
1. [DONE] Implement Tseep and Thrush onset detection function (ODF) from Vesper.

2. [DONE] Run Tseep, Thrush on 6 full night recordings. Export into 6 HDF5 containers by chunks. Parallelize over units.

3. [DONE] Apply ad hoc detector, with 100 thresholds and limits on duration, to Tseep and Thrush ODFs, on 6 full night recordings. Export peak times as 2*6*100=1200 CSV files. Parallelize over ODFs (2), units (6), and groups of 10 thresholds (10).

4. [DONE] Run clip suppressor on all CSV files. Export post-processed peak times as 2*6*100=1200 CSV files.

5. [DONE] Merge Thrush and Tseep predictions for every unit and every threshold, both with and without clip suppressor. It results in 2*6*100=1200 CSV files.

6. [DONE] Export metrics (n_selected, TP, FP, FN, precision, recall, F) for all 6 units, 3 detectors (Tseep, Thrush and both), and 10 tolerances, both with and without clip suppressor. It results in 6*3*10*2=360 CSV files.

7. [DONE] Compute global metrics (precision, recall, and F) across all 6 units and 10 tolerances. Store in 6 CSV files, 3 without suppressor, 3 with suppressor.


C. ICASSP model
1. [DONE] Generate BirdVox-70k dataset. Parallelize over units (6).

2. [DONE] Generate JAMS metadata. Parallelize over units (6).

3. [DONE] Augment audio data: 33 augmentations. Parallelize over augmentations (33).

4. [DONE] Store augmented audio into 6*33=198 HDF5 containers. Parallelize over units (6) and augmentations (33).

5. [DONE] Compute log-mel-spectrograms of augmented audio, store into 6*33=198 HDF5 containers. Parallelize over units (6) and augmentations (33).

6. [DONE] Compute log-mel-spectrograms of full night, store into 6 HDF5 containers. Parallelize over units (6).

7. [DONE] Train ICASSP convnet on BirdVox-70k with augmentation, 10 trials. Export 6*10=60 Keras models. Parallelize over folds (6) and trials (10).

8. [DONE] For every fold unit (6), every prediction unit in validation set and test set (3), export BirdVox-70k predictions as CSV files. Parallelize over folds (6), trials (10), and prediction units (3).

9. [DONE] For every fold unit (6), every mode (validation and test), compute metrics with data augmentation.

10. [DONE] For every fold (6), select the 5 trials that achieve the best validation accuracy, along with the corresponding threshold. For every unit, export best five trials, per-trial threshold, and per-trial metrics (n_selected, TP, FP, FN, TPR, TNR, accuracy, precision, recall, and F-measure) in 6 CSV files. Parallelize over units (6).

11. [DONE] For every possible combination of successive trials (5**6=15625), compute global metrics (n_selected, TP, FP, FN, TPR, TNR, accuracy, precision, recall, and F-measure) over the test set, with data augmentation.

12. [DONE] Train ICASSP convnet on BirdVox-70k without augmentation, 10 trials. Export 6*10=60 Keras models. Parallelize over folds (6) and trials (10).

13. [DONE] For every fold unit (6), every prediction unit in validation set and test set (3), export BirdVox-70k predictions as CSV files without data augmentation. Parallelize over folds (6), trials (10), and prediction units (3).

14. [DONE] For every fold unit (6), every mode (validation and test), compute metrics without data augmentation.

15. [DONE] Make a notebook displaying the quantiles of accuracy, both with and without data augmentation. Compute AUC and AUPRC.

16. [DONE] Investigate the locations of 20% of false detections.


D. Snowball on UrbanSound-8K
1. [DONE] Find padding heuristics (repeat vs zero).

2. [DONE] Augment UrbanSound-8K dataset.

3. [DONE] Compute scattering transform of augmented audio.

4. [DONE] Define snowball model and pescador generator.

5. [DONE] Train snowball convnet, one trial. Parallelize across folds (10).

6. [DONE] Compute snowball predictions. Parallelize across test folds (10) and prediction folds (2).

7. [DONE] Get validation accuracy, validation MRR, test accuracy, and test MRR, of snowball for one trial.


E. Cross-validated spherical k-means model
1. [DONE] Compute log-mel-spectrograms on 70k recordings. Parallelize across units (6).

2. [DONE] Train PCA on BirdVox-70k clips without augmentation. Save biases and PCA matrices. Parallelize across units (6).

3. [DONE] Train SKM on BirdVox-70k clips. Parallelize across units (6) and trials (10).

4. [DONE] Train SVM on BirdVox-70k. Parallelize across units (6), trials (10), and log10C (5).

5. [DONE] Compute predictions on 6 full night recordings.

6. [DONE] Postprocessing: peak-picking, thresholding, event matching.

7. [DONE] Export metrics (n_selected, TP, FP, FN, precision, recall, F)
for all 6 units, 10 tolerances, and 100 thresholds, to 6*10=60 CSV files.

8. [DONE] Compute global metrics (n_selected, TP, FP, FN, precision, recall, F and AUPRC) across all 6 units and 10 tolerances. Store in 1 CSV file.


F. Spectral flux
1. [DONE] Run spectral flux on 6 full night recordings. Export into 6 HDF5 containers by chunks. Parallelize over units.

2. [DONE] Apply spectral flux detector, with 100 thresholds, to spectral flux ODF, on 6 full night recordings. Export peak times as 6*100=600 CSV files. Parallelize over units (6) and groups of 10 thresholds (10).

3. [DONE] Export metrics (n_selected, TP, FP, FN, precision, recall, F) for all 6 units and 10 tolerances. It results in 6*10=60 CSV files.

4. [DONE] Compute global metrics (precision, recall, and F) across all 6 units and 10 tolerances. Store in 60 CSV files.


I. Dataset release
1. [DONE] Write README.

2. [DONE] Have consistent columns across units.

3. [DONE] Publish on Zenodo.

4. Bugfix latitude and longitude.

5. Add a text file with location of clips.

6. Publish on Zenodo under new name.


J. Per-channel energy normalization
1. [DONE] Compute PCEN on clips with augmentation. Parallelize over units (6) and instanced augmentations (31).

2. [DONE] Compute PCEN on full night data. Parallelize over units (6).

3. [DONE] Train PCEN convnets without augmentation. Parallelize over units (6) and trials (10).

4. [DONE] Predict PCEN convnets without augmentation on clips. Parallelize over units (6) and trials (10).

5. [IN PROGRESS] Predict PCEN convnets without augmentation on full night data. Parallelize over units (6) and trials (10).

6. [PENDING 5] Threshold PCEN convnet predictions without augmentation on full night data. Parallelize over units (6) and trials (10).

7. [DONE] Train PCEN convnets with augmentation. Parallelize over units (6) and trials (10).

8. [DONE] Predict PCEN convnets with augmentation on clips. Parallelize over units (6) and trials (10).

9. [READY] Predict PCEN convnets with augmentation on full night data. Parallelize over units (6) and trials (10).

10. Threshold PCEN convnet predictions with augmentation on full night data. Parallelize over units (6) and trials (10).

11. [IN PROGRESS] Train PCEN convnets with augmentation excepting noise. Parallelize over units (6) and trials (10).

12. [PENDING 11] Predict PCEN convnets with augmentation excepting noise on clips. Parallelize over units (6) and trials (10).

13. [PENDING 11] Predict PCEN convnets with augmentation excepting noise on full nights. Parallelize over units (6) and trials (10).

14. Threshold PCEN convnet predictions with augmentation excepting noise on full night data. Parallelize over units (6) and trials (10).


K. Dynamic filter networks
1. [DONE] Compute clip background logmelspec summaries. Parallelize over units (6) and instanced augmentations (31).

2. [DONE] Compute full night background logmelspec summaries. Parallelize over units (6).

3. [IN PROGRESS] Train adaptive threshold convnets without data augmentation. Parallelize over units (6) and trials (10).
!! re-run ./040_aug-all_trial-7.sh -8.sh -9.sh

4. [DONE] Train adaptive threshold convnets with data augmentation excepting noise. Parallelize over units (6) and trials (10).

5. [DONE] Train adaptive threshold convnets with data augmentation. Parallelize over units (6) and trials (10).

6. [DONE] Train dot-product convnets with data augmentation excepting noise. Parallelize over units (6) and trials (10).

7. [DONE] Train dot-product convnets with data augmentation. Parallelize over units (6) and trials (10).

8. [DONE] Train NTT convnets without data augmentation. Parallelize over units (6) and trials (10).

9. [DONE] Train NTT convnets with data augmentation excepting noise. Parallelize over units (6) and trials (10).

10. [DONE] Train NTT convnets with data augmentation. Parallelize over units (6) and trials (10).

11. [DONE] Predict NTT convnets on clips without augmentation. Parallelize over units (6) and trials (10).

12. [DONE] Predict NTT convnets on clips with augmentation excepting noise. Parallelize over units (6) and trials (10).

13. [DONE] Predict NTT convnets on clips with augmentation. Parallelize over units (6) and trials (10).

14. [DONE] Predict adaptive threshold convnets on clips without augmentation. Parallelize over units (6) and trials (10).

15. [DONE] Predict adaptive threshold convnets on clips with augmentation excepting noise. Parallelize over units (6) and trials (10).

16. [DONE] Predict adaptive threshold convnets on clips with augmentation. Parallelize over units (6) and trials (10).

17. [IN PROGRESS] Predict NTT convnets on full nights without augmentation. Parallelize over units (6) and trials (10).

18. [IN PROGRESS] Predict NTT convnets on full nights with augmentation excepting noise. Parallelize over units (6) and trials (10).

19. [IN PROGRESS] Predict NTT convnets on full nights with augmentation. Parallelize over units (6) and trials (10).

20. [PENDING 17] Threshold NTT convnets on full nights without augmentation. Parallelize over units (6) and trials (10).

21. [PENDING 18] Threshold NTT convnets on full nights with augmentation excepting noise. Parallelize over units (6) and trials (10).

22. [PENDING 19] Threshold NTT convnets on full nights with augmentation. Parallelize over units (6) and trials (10).


L. Dynamic filter networks with PCEN
1. [DONE] Compute clip background PCEN summaries. Parallelize over units (6) and instanced augmentations (31).

2. [IN PROGRESS] Compute full night background PCEN summaries. Parallelize over units (6).

3. [DONE] Train NTT PCEN convnets without data augmentation. Parallelize over units (6) and trials (10).

4. [DONE] Train NTT PCEN convnets with data augmentation excepting noise. Parallelize over units (6) and trials (10).

5. [DONE] Train NTT PCEN convnets with data augmentation. Parallelize over units (6) and trials (10).

6. [DONE] Train PCEN convnets with adaptive threshold, without data augmentation. Parallelize over units (6) and trials (10).

7. [IN PROGRESS] Train PCEN convnets with adaptive threshold, with augmentation excepting noise. Parallelize over units (6) and trials (10).

8. [IN PROGRESS] Train PCEN convnets with adaptive threshold, with augmentation. Parallelize over units (6) and trials (10).

9. [READY] Predict NTT PCEN convnets without data augmentation on clips. Parallelize over units (6) and trials (10).

10. [READY] Predict NTT PCEN convnets with data augmentation excepting noise on clips. Parallelize over units (6) and trials (10).

11. [READY] Predict NTT PCEN convnets with data augmentation on clips. Parallelize over units (6) and trials (10).

12. [READY] Predict NTT PCEN convnets without data augmentation on full nights. Parallelize over units (6) and trials (10).

13. [READY] Predict NTT PCEN convnets with data augmentation excepting noise on full nights. Parallelize over units (6) and trials (10).

14. [READY] Predict NTT PCEN convnets with data augmentation on full nights. Parallelize over units (6) and trials (10).

15. [PENDING 12] Threshold NTT PCEN convnets without data augmentation on full nights. Parallelize over units (6) and trials (10).

16. [PENDING 13] Threshold NTT PCEN convnets with data augmentation excepting noise on full nights. Parallelize over units (6) and trials (10).

17. [PENDING 14] Threshold NTT PCEN convnets with data augmentation on full nights. Parallelize over units (6) and trials (10).
