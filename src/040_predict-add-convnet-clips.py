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
n_input_hops = 104
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
print("Using additive context-aware convnet for binary classification in " +
    dataset_name + " clips with logmelspec input. ")
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
model_name = "icassp-add-convnet"
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
aug_str = "original"
logmelspec_dir = os.path.join(data_dir,
    "_".join([dataset_name, "clip-logmelspec"]))
original_logmelspec_dir = os.path.join(logmelspec_dir, aug_str)
hdf5_name = "_".join([dataset_name, aug_str, predict_unit_str])
hdf5_path = os.path.join(original_logmelspec_dir, hdf5_name + ".hdf5")
lms_container = h5py.File(hdf5_path, "r")
lms_group = lms_container["logmelspec"]
keys = list(lms_group.keys())


# Open background container with h5py.
bg_name = "_".join(
    [dataset_name, "clip-logmelspec-backgrounds"])
bg_dir = os.path.join(data_dir, bg_name)
T_str = "T-" + str(bg_duration).zfill(4)
T_dir = os.path.join(bg_dir, T_str)
bg_name = "_".join(
    [dataset_name, "background_summaries",
     test_unit_str, T_str + ".hdf5"])
bg_path = os.path.join(T_dir, bg_name)
bg_container = h5py.File(bg_path, "r")
bg_group = bg_container["logmelspec_background"]


# Create HDF5 container for predictions.
clip_predictions_name = "_".join([
    dataset_name,
    model_name,
    "test-" + test_unit_str,
    "predict-" + predict_unit_str,
    "clip-predictions"
])


# Create CSV file.
prediction_name = "_".join([dataset_name, model_name,
    "test-" + test_unit_str, trial_str, "predict-" + predict_unit_str,
    "clip-predictions"])
prediction_path = os.path.join(trial_dir, prediction_name + ".csv")
csv_file = open(prediction_path, 'w')
csv_writer = csv.writer(csv_file, delimiter=',')


# Create CSV header.
csv_header = ["Dataset", "Test unit", "Prediction unit", "Timestamp",
    "Frequency (Hz)", "Augmentation", "Key", "Ground truth", "Predicted probability"]
csv_writer.writerow(csv_header)


# Loop over keys.
for key in keys:
    # Load logmelspec.
    X_lms = lms_group[key]

    # Trim logmelspec in time to required number of hops.
    X_width = X_lms.shape[1]
    first_col = int((X_width-n_input_hops) / 2)
    last_col = int((X_width+n_input_hops) / 2)
    X_lms = X_lms[:, first_col:last_col]

    # Add trailing singleton dimension for Keras interoperability.
    X_lms = X_lms[np.newaxis, :, :, np.newaxis]

    # Define key for background container.
    bg_key = "_".join(key.split("_")[:-1])

    # Load background.
    X_bg = bg_group[bg_key].value.T
    X_bg = X_bg[np.newaxis, :, :]

    # Predict.
    predicted_probability = model.predict(
        {"spec_input": X_lms, "bg_input": X_bg})[0, 0]

    # Store prediction as DataFrame row.
    key_split = key.split("_")
    timestamp_str = key_split[1]
    freq_str = key_split[2]
    ground_truth_str = key_split[3]
    aug_str = key_split[4]
    predicted_probability_str = "{:.16f}".format(predicted_probability)
    row = [dataset_name, test_unit_str, predict_unit_str, timestamp_str,
         freq_str, aug_str, key, ground_truth_str, predicted_probability_str]
    csv_writer.writerow(row)


# Close HDF5 containers.
lms_container.close()
bg_container.close()


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
