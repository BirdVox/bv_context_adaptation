import csv
import datetime
import h5py
import keras
import numpy as np
import os
import pandas as pd
import sys
import tensorflow as tf
import time

import localmodule


# Define constants.
data_dir = localmodule.get_data_dir()
dataset_name = localmodule.get_dataset_name()
folds = localmodule.fold_units()
models_dir = localmodule.get_models_dir()
clip_length = 104
hop_length = 34
hop_duration = hop_length * 32 / 22050
bg_duration = 1800


# Read command-line arguments.
args = sys.argv[1:]
aug_kind_str = args[0]
test_unit_str = args[1]
trial_str = args[2]
predict_unit_str = args[3]


# Retrieve fold such that unit_str is in the test set.
fold = [f for f in folds if test_unit_str in f[0]][0]
test_units = fold[0]
training_units = fold[1]
validation_units = fold[2]


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Using NTT-like convnet for detection in " +
    dataset_name + ", full audio, with logmelspec input. ")
print("Training set: " + ", ".join(training_units) + ".")
print("Validation set: " + ", ".join(validation_units) + ".")
print("Test set: " + ", ".join(test_units) + ".")
print("")
print('h5py version: {:s}'.format(h5py.__version__))
print('keras version: {:s}'.format(keras.__version__))
print('numpy version: {:s}'.format(np.__version__))
print('tensorflow version: {:s}'.format(tf.__version__))
print("")


# Load model.
model_name = "icassp-ntt-convnet"
if not aug_kind_str == "none":
    model_name = "_".join([model_name, "aug-" + aug_kind_str])
model_dir = os.path.join(models_dir, model_name)
unit_dir = os.path.join(model_dir, test_unit_str)
trial_dir = os.path.join(unit_dir, trial_str)
network_name = "_".join(
    [dataset_name, model_name, test_unit_str, trial_str, "network"])
network_path = os.path.join(trial_dir, network_name + ".hdf5")
model = keras.models.load_model(network_path)


# Open logmelspec container with h5py.
lms_dir = os.path.join(data_dir, "_".join([dataset_name, "full-logmelspec"]))
hdf5_path = os.path.join(lms_dir, predict_unit_str + ".hdf5")
lms_container = h5py.File(hdf5_path, "r")
lms_group = lms_container["logmelspec"]


# Open background container with h5py.
bg_dir = os.path.join(data_dir, "_".join([
    dataset_name, "full-logmelspec-backgrounds"]))
bg_duration_str = str(int(bg_duration)).zfill(4)
T_name = "-".join(["T", str(bg_duration_str)])
bg_T_dir = os.path.join(bg_dir, T_name)
out_unit_name = "_".join([
    dataset_name, "full-backgrounds",
    predict_unit_str, T_name]) + ".hdf5"
bg_unit_path = os.path.join(bg_T_dir, out_unit_name)
bg_unit_file = h5py.File(bg_unit_path, "r")
bg_group = bg_unit_file["logmelspec_background"]


# Create CSV file.
prediction_name = "_".join([dataset_name, model_name,
    "test-" + test_unit_str, trial_str, "predict-" + predict_unit_str,
    "full-predictions"])
prediction_path = os.path.join(trial_dir, prediction_name + ".csv")
csv_file = open(prediction_path, 'w')
csv_writer = csv.writer(csv_file, delimiter=',')


# Create CSV header.
csv_header = ["Dataset", "Model", "Test unit", "Prediction unit", "Timestamp",
    "Predicted probability"]
csv_writer.writerow(csv_header)


# Compute number of hops.
n_cols = lms_group.shape[1]
n_hops = int(n_cols / hop_length) - 1
is_end_reached = False
n_bg_cols = bg_group.shape[-1]
bg_ratio = n_bg_hops / n_cols


# Loop over hops.
for hop_id in range(n_hops):

    # Load clip in full LMS data.
    clip_start = hop_id * hop_length
    clip_stop = clip_start + clip_length
    if clip_stop > n_cols:
        is_end_reached = True
        clip_stop = n_hops
        clip_start = clip_stop - clip_length


    if not is_end_reached:
        # Load logmelspec
        X_lms = lms_group[:, clip_start:clip_stop]
        X_lms = X_lms[np.newaxis, :, :, np.newaxis]

        # Load background.
        bg_col = min(
            int(np.round(bg_ratio * clip_start)), n_bg_cols-1)
        X_bg = bg_group[:, :, bg_col].T
        X_bg = X_bg[np.newaxis, :, :]

        # Predict.
        predicted_probability = model.predict(
            {"spec_input": X_lms, "bg_input": X_bg})[0, 0]


    # Store prediction as DataFrame row.
    timestamp = (hop_id+1) * hop_duration
    timestamp_str = "{:9.3f}".format(timestamp)
    predicted_probability_str = "{:.16f}".format(predicted_probability)
    row = [dataset_name, model_name, test_unit_str, predict_unit_str,
        timestamp_str, predicted_probability_str]
    csv_writer.writerow(row)


# Close CSV file.
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
