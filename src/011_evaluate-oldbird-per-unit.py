import datetime
import h5py
import mir_eval
import numpy as np
import os
import pandas as pd
import sys
import time

import localmodule


# Define constants.
data_dir = localodule.get_data_dir()
dataset_name = localmodule.get_datset_name()
models_dir = localmodule.get_models_dir()
negative_labels = localmodule.get_negative_labels()
tolerances = localmodule.get_tolerances()
n_thresholds = 100


# Read command-line arguments.                           ENABLE
#args = sys.argv[1:]
#unit_str = args[0]
#odf_str = args[1]
#suppressor_str = args[2]
unit_str = "unit01"
odf_str = "thrush"
clip_suppressor_str = "clip-suppressor"


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Evaluating Old Bird on " + dataset_name + ", " + unit_str + ".")
print('h5py version: {:s}'.format(h5py.__version__))
print('mir_eval version: {:s}'.format(mir_eval.__version__))
print('numpy version: {:s}'.format(np.__version__))
print('pandas version: {:s}'.format(pd.__version__))
print("")


# Define directory for predictions.
oldbird_models_dir = os.path.join(models_dir, "oldbird")
unit_dir = os.path.join(oldbird_models_dir, unit_str)
predictions_name = "_".join(["predictions", clip_suppressor_str])
predictions_dir = os.path.join(unit_dir, predictions_name)


# Open annotation as Pandas DataFrame.
annotations_name = "_".join([dataset_name, "annotations"])
annotations_dir = os.path.join(data_dir, annotations_name)
annotation_name = unit_str + ".txt"
annotation_path = os.path.join(annotations_dir, annotation_name)
ann_df = pd.read_csv(annotation_path, delimiter="\t")


# Restrict rows to negative labels.
if "Calls" in ann_df.columns:
    ann_df = ann_df.loc[~ann_df["Calls"].isin(negative_labels)]


# Restrict rows to frequency range of interest.
if odf_str in ["thrush", "tseep"]:
    oldbird_data_name = "_".join([dataset_name, "oldbird"])
    oldbird_data_dir = os.path.join(data_dir, oldbird_data_name)
    oldbird_data_path = os.path.join(oldbird_data_dir, unit_str + ".hdf5")
    oldbird_hdf5 = h5py.File(oldbird_data_path, "r")
    settings_key = "_".join([odf_str, "settings"])
    settings = oldbird_hdf5[settings_key]
    filter_f0 = settings["filter_f0"].value
    filter_f1 = settings["filter_f1"].value
    ann_df = ann_df[
        0.5*(ann_df["Low Freq (Hz)"]+ann_df["High Freq (Hz)"] > filter_f0 &
        0.5*(ann_df["Low Freq (Hz)"]+ann_df["High Freq (Hz)"] < filter_f1]


begin_times = np.array(annotation["Begin Time (s)"]])
end_times = np.array(annotation["End Time (s)"])
true_times = 0.5 * (begin_times+end_times)


# Loop over tolerances.
tolerance = tolerances[0] #                             DISABLE
# for tolerance in tolerances:                           ENABLE

# Loop over thresholds.
threshold_id = 0 #                                      DISABLE
# for threshold_id in range(n_threshold):               ENABLE

# Load prediction.
threshold_str = "th-" + str(threshold_id).zfill(2)
prediction_name_components = [dataset_name, "oldbird", odf_str,
    threshold_str, "predictions"]
if clip_suppressor_str == "clip_suppressor":
    prediction_name_components.append(clip_suppressor_str)
prediction_name = "_".join(prediction_name_components) + ".csv"
prediction_path = os.path.join(predictions_dir, prediction_name)
prediction_df = pd.read_csv(prediction_path)
predicted_times = prediction_df["Time (s)"]


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
