import datetime
import h5py
import numpy as np
import os
import pandas as pd
import sys
import time

import localmodule


# Define constants.
data_dir = localmodule.get_data_dir()
dataset_name = localmodule.get_dataset_name()
models_dir = localmodule.get_models_dir()
oldbird_models_dir = os.path.join(models_dir, "oldbird")
units = localmodule.get_units()
odfs = ["thrush", "tseep"]
n_thresholds = 100


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Running Old Bird clip suppressor on " + dataset_name + ".")
print('h5py version: {:s}'.format(h5py.__version__))
print('numpy version: {:s}'.format(np.__version__))
print('pandas version: {:s}'.format(pd.__version__))
print("")


# Loop over units.
for unit_str in units:

    # Define input and output folder.
    unit_dir = os.path.join(oldbird_models_dir, unit_str)
    in_predictions_name = "_".join(["predictions", "no-clip-suppressor"])
    in_predictions_dir = os.path.join(unit_dir, in_predictions_name)
    out_predictions_name = "_".join(["predictions", "clip-suppressor"])
    out_predictions_dir = os.path.join(unit_dir, out_predictions_name)
    os.makedirs(out_predictions_dir, exist_ok=True)

    # Loop over ODFs (Thrush and Tseep)
    for odf_str in odfs:

        # Define suppressor count threshold and period.
        oldbird_data_name = "_".join([dataset_name, "oldbird"])
        oldbird_data_dir = os.path.join(data_dir, oldbird_data_name)
        oldbird_data_path = os.path.join(oldbird_data_dir, unit_str + ".hdf5")
        oldbird_hdf5 = h5py.File(oldbird_data_path, "r")
        settings_key = "_".join([odf_str, "settings"])
        settings = oldbird_hdf5[settings_key]
        suppressor_count_threshold = settings["suppressor_count_threshold"].value
        suppressor_period = settings["suppressor_period"].value

        # Loop over thresholds.
        for threshold_id in range(n_thresholds):
            # Define input prediction path.
            threshold_str = "th-" + str(threshold_id).zfill(2)
            in_prediction_name = "_".join(
                [dataset_name, "oldbird", odf_str,
                 unit_str, threshold_str, "predictions.csv"])
            in_prediction_path = os.path.join(
                in_predictions_dir, in_prediction_name)

            # Define output prediction path.
            out_prediction_name = "_".join(
                [dataset_name, "oldbird", odf_str,
                 unit_str, threshold_str, "predictions_clip-suppressor.csv"])
            out_prediction_path = os.path.join(
                out_predictions_dir, out_prediction_name)

            # Read input CSV file as Pandas DataFrame.
            in_df = pd.read_csv(in_prediction_path)

            # Convert column of timestamps to NumPy array
            in_times = np.array(in_df["Time (s)"])

            # Initialize variables.
            n_rows = len(in_times)
            n = 0
            out_times = []

            # Loop over rows.
            while n < (n_rows-suppressor_count_threshold):
                current_time = in_times[n]
                next_n = n + suppressor_count_threshold
                next_time = in_times[next_n]
                time_difference = next_time - current_time
                if time_difference < suppressor_period:
                    while time_difference < suppressor_period:
                        next_n = next_n + 1
                        next_time = in_times[next_n]
                        time_difference = next_time - current_time
                    n = next_n
                else:
                    out_times.append(current_time)
                    n = n + 1

            # Select rows in input DataFrame.
            out_df = in_df[in_df["Time (s)"].isin(out_times)]

            # Export output DataFrame to CSV.
            out_df.to_csv(out_prediction_path)


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
