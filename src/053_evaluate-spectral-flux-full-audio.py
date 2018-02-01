import h5py
import mir_eval
import numpy as np
import os
import pandas as pd
import peakutils
import sys
import localmodule


# Define directory of spectral flux ODFs.
data_dir = localmodule.get_data_dir()
dataset_name = localmodule.get_dataset_name()
models_dir = localmodule.get_models_dir()
units = localmodule.get_units()
n_units = len(units)
sf_dir = os.path.join(
    data_dir,
    "_".join([dataset_name, "spectral-flux"]))


# Define constants.
sf_sr = 22050
sf_hop_length = 512
n_thresholds = 100
min_dist = 4
tolerance = 0.5


# Parse arguments.
args = sys.argv[1:]
test_unit_str = args[0]


# Define array of thresholds.
thresholds = np.linspace(0.0, 0.5, n_thresholds)


# Define directory for annotations.
annotations_name = "_".join([dataset_name, "annotations"])
annotations_dir = os.path.join(data_dir, annotations_name)


# Initialize arrays
tp_matrix = np.zeros((n_thresholds, n_units))
fp_matrix = np.zeros((n_thresholds, n_units))
fn_matrix = np.zeros((n_thresholds, n_units))


# Load onset detection function.
odf_path = os.path.join(sf_dir, test_unit_str + ".hdf5")
odf_file = h5py.File(odf_path, "r")
odf = odf_file["spectral-flux_odf"].value
odf = np.ravel(odf)
odf_file.close()


# Load annotation.
annotation_path = os.path.join(
annotations_dir, test_unit_str + ".txt")
annotation = pd.read_csv(annotation_path, '\t')
begin_times = np.array(annotation["Begin Time (s)"])
end_times = np.array(annotation["End Time (s)"])
relevant = 0.5 * (begin_times + end_times)
relevant = np.sort(relevant)
n_relevant = len(relevant)


# Create CSV file for metrics.
model_dir = os.path.join(
    models_dir, "spectral-flux")
test_unit_dir = os.path.join(
    model_dir, test_unit_str)
metrics_name = "_".join([
    dataset_name,
    model_name,
    "test-" + test_unit_str,
    "full-audio-metrics"])
metrics_path = os.path.join(
    test_unit_dir, metrics_name + ".csv")


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


# Write row.
csv_file = open(metrics_path, 'w')
csv_writer = csv.writer(csv_file, delimiter=',')
csv_writer.writerow(csv_header)
csv_file.close()


# Loop over thresholds.
for th_id, threshold in tqdm(enumerate(thresholds)):
    # Pick peaks.
    peak_locs = peakutils.indexes(
        odf, thres=threshold, min_dist=4)
    selected = peak_locs * sf_hop_length / sf_sr

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
        format(threshold, ".10f"),
        str(n_relevant).rjust(5),
        str(n_selected).rjust(6),
        str(true_positives).rjust(5),
        str(false_positives).rjust(6),
        str(false_negatives).rjust(5),
        format(precision, ".6f").rjust(10),
        format(recall, ".6f").rjust(10),
        format(f1_score, ".6f").rjust(10)
    ]

    # Write row.
    csv_file = open(metrics_path, 'a')
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(row)
    csv_file.close()


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
