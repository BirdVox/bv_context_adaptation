A. Spherical k-means model
1. [DONE] Train on external data.

2. [DONE] Compute predictions on 6 full night recordings.

3. [DONE] Postprocessing: peak-picking, thresholding, event matching.

4. [DONE] Export metrics (n_selected, TP, FP, FN, precision, recall, F)
for all 6 units, 10 tolerances, and 100 thresholds, to 6*10=60 CSV files.

5. [DONE] Compute global metrics (precision, recall, F and AUPRC) across all 6 units and 10 tolerances. Store in 1 CSV file.


B. Old Bird
1. [DONE] Implement Tseep and Thrush onset detection function (ODF) from Vesper.

2. [IN PROGRESS] Run Tseep, Thrush on 6 full night recordings. Export as
numPy matrices of 10-minute chunks. Also export a linear combination of
Tseep and Thrush ODFs (hereafter called OldBird-mixed) that will be used
to compute AUPRC.

3. Apply ad hoc detector, with fixed threshold and limits on duration,
to Tseep and Thrush ODFs, on 6 full night recordings. Export peak times
as 2*6=12 CSV files.

4. Export metrics (n_selected, TP, FP, FN, precision, recall, F) for all 6
units, 3 detectors (Tseep, Thrush and both), and 10 tolerances. It results
in 6*3*10=180 CSV files.

5. Compute global metrics (precision, recall, and F) across all 6 units and
10 tolerances. Store in 1 CSV file.

6. Apply OldBird-mixed detector, with 100 different thresholds and limits
on duration, on 6 full night recordings and 10 tolerances. It results in
6*10=60 CSV files.

7. Compute global AUPRC across all 6 units for OldBird-mixed detector. Store in 1 CSV file.


C. Deep learning
1. [DONE] Generate BirdVox-70k dataset.

2. [DONE] Generate JAMS metadata.

3. [DONE] Augment audio data: 33 augmentations.

4. [DONE] Store augmented audio into 6*33=198 HDF5 containers.

5. [IN PROGRESS] Compute log-mel-spectrograms of augmented audio, store into 6*33=198 HDF5 containers.

6. Compute log-mel-spectrograms of full night, store into 6 HDF5 containers.

7. ICASSP convnet without data augmentation: for all 6 units and 10 tolerances, train (a), predict (b), evaluate on BirdVox-70k (c), evaluate on full nights (d).

8. ICASSP convnet with data augmentation: for all 6 units and 10 tolerances, train (a), predict (b), evaluate on BirdVox-70k (c), evaluate on full nights (d).


D. Snowball on UrbanSound-8K
1. [DONE] Augment UrbanSound-8K dataset.

2. [IN PROGRESS] Compute scattering transform of augmented audio.

3. Define snowball model and pescador generator.

4. Snowball convnet: train (a), predict (b), evaluate (c).