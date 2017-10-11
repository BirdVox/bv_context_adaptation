import csv
import datetime
import h5py
import numpy as np
import os
import pandas as pd
import sklearn.metrics
import sys
import time

import localmodule


# Read command-line arguments.
args = sys.argv[1:]
aug_kind_str = args[0]
test_unit_str = args[1]
trial_id = int(args[2])
predict_unit_str = args[3]
thresholds_str = args[4]
threshold_id_start = int(thresholds_str[3:5])
threshold_id_stop = int(thresholds_str[-2:])
threshold_id_range = range(threshold_id_start, 1 + threshold_id_stop)


# Define constants.
data_dir = localmodule.get_data_dir()
dataset_name = localmodule.get_dataset_name()
folds = localmodule.fold_units()
models_dir = localmodule.get_models_dir()
units = localmodule.get_units()
model_name = "icassp-convnet"
if not aug_kind_str == "none":
    model_name = "_".join([model_name, "aug-" + aug_kind_str])
model_dir = os.path.join(models_dir, model_name)
icassp_thresholds = 1.0 - np.concatenate((
    np.logspace(-9, -2, 141), np.delete(np.logspace(-2, 0, 81), 0)
))
n_thresholds = len(icassp_thresholds)
tolerance = 0.5 # in seconds


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Thresholding Salamon's ICASSP 2017 convnet for detection in " +
    dataset_name + " full audio. ")
print("Augmentation kind: " + aug_kind_str)
print("Test unit: " + test_unit_str)
print("Trial ID: {}".format(trial_id))
print("Prediction unit: " + predict_unit_str)
print("Thresholds " + thresholds_str)
print("")
print('h5py version: {:s}'.format(h5py.__version__))
print('numpy version: {:s}'.format(np.__version__))
print('pandas version: {:s}'.format(pd.__version__))
print('scikit-learn version: {:s}'.format(sklearn.__version__))
print("")


# Define directory for test unit.
unit_dir = os.path.join(model_dir, test_unit_str)


# Define directory for trial.
trial_str = "trial-" + str(trial_id)
trial_dir = os.path.join(unit_dir, trial_str)


# Create directory for metrics.
metrics_dir = os.path.join(trial_dir, "metrics")
os.makedirs(metrics_dir, exist_ok=True)


# Load ODF.
prediction_name = "_".join([
    dataset_name,
    model_name,
    "test-" + test_unit_str,
    trial_str,
    "predict-" + test_unit_str,
    "full-predictions.csv"])
prediction_path = os.path.join(trial_dir, prediction_name)
prediction_df = pd.read_csv(prediction_path)
odf = np.array(prediction_df["Predicted probability"])
timestamps = np.array(prediction_df["Timestamp"])


# Load annotation.
annotations_name = "_".join([dataset_name, "annotations"])
annotations_dir = os.path.join(data_dir, annotations_name)
annotation_path = os.path.join(annotations_dir, test_unit_str + ".txt")
annotation = pd.read_csv(annotation_path, "\t")
begin_times = np.array(annotation["Begin Time (s)"])
end_times = np.array(annotation["End Time (s)"])
relevant = 0.5 * (begin_times + end_times)
relevant = np.sort(relevant)
n_relevant = len(relevant)


# Create CSV file for metrics.
metrics_name = "_".join([
    dataset_name,
    model_name,
    test_unit_str,
    "full-audio-metrics"
])
metrics_path = os.path.join(metrics_dir, metrics_name + ".csv")
csv_file = open(metrics_path, 'w')
csv_writer = csv.writer(csv_file, delimiter=',')


# Write CSV header.
csv_header = [
    "Dataset",
    "Augmentation kind",
    "Test unit",
    "Trial",
    "Prediction unit",
    "Tolerance",
    "Threshold",
    "Relevant",
    "Selected",
    "True positives",
    "False positives",
    "False negatives",
    "Precision (%)",
    "Recall (%)",
    "F1 Score (%)"]
csv_writer.writerow(csv_header)


# Loop over thresholds.
for threshold_id in threshold_id_range:
    threshold = icassp_thresholds[threshold_id]

    # Pick peaks.
    peak_locations = peakutils.indexes(odf, thres=threshold, min_dist=min_dist)
    peak_times = timestamps[peak_locations]
    peak_values = odf[peak_locations]
    selected = peak_times[peak_values > threshold]

    # Match events.
    selected_relevant = mir_eval.util.match_events(
        relevant, selected, tolerance)

    # Count TP, FP, and FN.
    true_positives = len(selected_relevant)
    n_selected = len(selected)
    false_positives = n_selected - true_positives
    false_negatives = n_relevant - true_positives

    # Compute precision, recall, and F1 score.
    if n_selected == 0 or true_positives == 0:
        precision = 0.0
        recall = 0.0
        f1_score = 0.0
    else:
        precision = 100 * true_positives / n_selected
        recall = 100 * true_positives / n_relevant
        f1_score = 2*precision*recall / (precision+recall)

    # Write row.
    row = [
        dataset_name,
        aug_kind_str,
        test_unit_str,
        str(trial_id),
        predict_unit_str,
        str(int(np.round(1000*tolerance))).rjust(4),
        format(threshold, ".9f"),
        str(relevant).rjust(5),
        str(selected).rjust(6),
        str(true_positives).rjust(5),
        str(false_positives).rjust(5),
        str(false_negatives).rjust(5),
        format(precision, ".6f"),
        format(recall, ".6f"),
        format(f1_score, ".6f")
    ]


# Print elapsed time.
print(str(datetime.datetime.now()) + " Finish.")
elapsed_time = time.time() - int(start_time)
elapsed_hours = int(elapsed_time / (60 * 60))
elapsed_minutes = int((elapsed_time % (60 * 60)) / 60)
elapsed_seconds = elapsed_time % 60.
elapsed_str = "{:>02}:{:>02}:{:>05.2f}".format(elapsed_hours,
                                               elapsed_minutes,
                                               elapsed_seconds)
print("Total elapsed time: " + elapsed_str + ".")
