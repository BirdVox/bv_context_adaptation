A. Spherical k-means model
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

4. [DONE] Run clip suppressor on all CSV files. Export post-processed peak times as 2*6=12 CSV files. Parallelize over ODFs (2) and units (6).

5. Export metrics (n_selected, TP, FP, FN, precision, recall, F) for all 6
units, 3 detectors (Tseep, Thrush and both), and 10 tolerances, both with and without clip suppressor. It results in 6*3*10*2=360 CSV files.

6. Compute global metrics (precision, recall, and F) across all 6 units and
10 tolerances. Store in 2 CSV file, one without suppressor, one with suppressor.

6. Apply OldBird-mixed detector, with 100 different thresholds and limits
on duration, on 6 full night recordings and 10 tolerances. It results in 6*10=60 CSV files.

7. Compute global AUPRC across all 6 units for OldBird-mixed detector. Store in 1 CSV file.


C. Deep learning
1. [DONE] Generate BirdVox-70k dataset. Parallelize over units (6).

2. [DONE] Generate JAMS metadata. Parallelize over units (6).

3. [DONE] Augment audio data: 33 augmentations. Parallelize over augmentations (33).

4. [DONE] Store augmented audio into 6*33=198 HDF5 containers. Parallelize over units (6) and augmentations (33).

5. [DONE] Compute log-mel-spectrograms of augmented audio, store into 6*33=198 HDF5 containers. Parallelize over units (6) and augmentations (33).

6. [DONE] Compute log-mel-spectrograms of full night, store into 6 HDF5 containers. Parallelize over units (6).

7. Train icassp convnet on BirdVox-70k. Export 6*10=60 Keras models. Parallelize over units (6) and trials (10).

8. For every trained unit (6), every prediction unit (6), and every trial (10), export 6*10=60 BirdVox-70k predictions as HDF5 containers. Compute metrics (n_selected, TP, FP, FN, TPR, TNR, accuracy, precision, recall, and F-measure) for 100 different thresholds. Parallelize over trained units (6) and trials (10).

8. For every trained unit (6), select the 5 trials that achieve the best validation accuracy, along with the corresponding threshold. For every unit, export best five trials, per-trial threshold, and per-trial metrics (n_selected, TP, FP, FN, TPR, TNR, accuracy, precision, recall, and F-measure) in 6 CSV files. Parallelize over units (6).

9. For every possible combination of successive trials (5**6=15625), compute global metrics (n_selected, TP, FP, FN, TPR, TNR, accuracy, precision, recall, and F-measure) over the test set.

10. Make a notebook displaying the quantiles of accuracy. Compute AUC and AUPRC.


D. Snowball on UrbanSound-8K
1. [DONE] Augment UrbanSound-8K dataset.

2. [DONE] Compute scattering transform of augmented audio.

3. Define snowball model and pescador generator.

4. Snowball convnet: train (a), predict (b), evaluate (c).


Juan: schedule C, then B, then D, then A.