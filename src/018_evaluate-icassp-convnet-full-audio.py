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


# Create CSV file for metrics.
metrics_name = "_".join([
    dataset_name,
    model_name,
    test_unit_str,
    "clip-metrics"
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
    "Ad hoc threshold",
    "Ad hoc validation TP",
    "Ad hoc validation FP",
    "Ad hoc validation TN",
    "Ad hoc validation FN",
    "Ad hoc validation accuracy (%)",
    "Ad hoc test TP",
    "Ad hoc test FP",
    "Ad hoc test TN",
    "Ad hoc test FN",
    "Ad hoc test accuracy (%)",
    "Cross-validated threshold",
    "Cross-validated validation TP",
    "Cross-validated validation FP",
    "Cross-validated validation TN",
    "Cross-validated validation FN",
    "Cross-validated validation accuracy (%)",
    "Cross-validated test TP",
    "Cross-validated test FP",
    "Cross-validated test TN",
    "Cross-validated test FN",
    "Oracle threshold",
    "Test oracle TP",
    "Test oracle FP",
    "Test oracle TN",
    "Test oracle FN",
    "Test oracle accuracy (%)",
    "Validation AUC",
    "Test AUC"]
csv_writer.writerow(csv_header)




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
