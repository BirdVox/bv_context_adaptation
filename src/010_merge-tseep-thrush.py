import datetime
import os
import pandas as pd
import sys
import time

import localmodule


# Define constants.
dataset_name = localmodule.get_dataset_name()
models_dir = localmodule.get_models_dir()
oldbird_model_dir = os.path.join(models_dir, "oldbird")
units = localmodule.get_units()
clip_suppressor_modes = ["no-clip-suppressor", "clip-suppressor"]
n_thresholds = 100


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Merge Tseep and Thrush predictions in " + dataset_name + ".")
print('pandas version: {:s}'.format(pd.__version__))
print("")


# Loop over units.
for unit_str in units:
    unit_dir = os.path.join(oldbird_model_dir, unit_str)

    # Loop over clip suppressor modes.
    for clip_suppressor_str in clip_suppressor_modes:
        prediction_name = "_".join(["predictions", clip_suppressor_str])
        prediction_dir = os.path.join(unit_dir, prediction_name)

        # Loop over thresholds.
        for threshold_id in range(n_thresholds):
            threshold_str = "th-" + str(threshold_id).zfill(2)

            # Load Thrush prediction.
            thrush_components_list = [
                dataset_name,
                "oldbird",
                "thrush",
                unit_str,
                threshold_str,
                "predictions"
            ]
            if clip_suppressor_str == "clip-suppressor":
                thrush_components_list.append(clip_suppressor_str)
            thrush_prediction_name = "_".join(thrush_components_list)
            thrush_prediction_path = os.path.join(
                prediction_dir, thrush_prediction_name + ".csv")
            thrush_df = pd.read_csv(thrush_prediction_path)

            # Load Tseep prediction.
            tseep_components_list = thrush_components_list
            tseep_components_list[2] = "tseep"
            tseep_prediction_name = "_".join(tseep_components_list)
            tseep_prediction_path = os.path.join(
                prediction_dir, tseep_prediction_name + ".csv")
            tseep_df = pd.read_csv(tseep_prediction_path)

            # Merge Thrush and Tseep predictions.
            merged_df = pd.concat((thrush_df, tseep_df))
            merged_df = merged_df.sort_values(["Time (s)"])

            # Export merged predictions as CSV.
            merged_components_list = thrush_components_list
            merged_components_list[2] = "merged"
            merged_prediction_name = "_".join(merged_components_list)
            merged_prediction_path = os.path.join(
                prediction_dir, merged_prediction_name + ".csv")
            merged_df.to_csv(merged_prediction_path)


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
