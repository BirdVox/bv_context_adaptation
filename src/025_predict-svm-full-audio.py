import csv
import datetime
import h5py
from sklearn.externals import joblib
import numpy as np
import os
import pandas as pd
import pickle
import sklearn.preprocessing
import sklearn.svm
import skm
import sys
import time

sys.path.append("../src")
import localmodule


# Define constants.
data_dir = localmodule.get_data_dir()
dataset_name = localmodule.get_dataset_name()
patch_width = 32
n_patches_per_clip = 1
aug_str = "original"
instanced_aug_str = aug_str
clip_length = 104
hop_length = 34
hop_duration = hop_length * 32 / 22050
patch_width = 32
n_patches_per_clip = 3
chunk_size = 10000


# Parse arguments.
args = ["unit05", "6"]
test_unit_str = args[0]
trial_id = int(args[1])


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Running probabilistic SVM on " + dataset_name + " full audio.")
print("Test unit: " + test_unit_str + ".")
print("Trial ID: " + str(trial_id) + ".")
print("")
print("h5py version: {:s}".format(h5py.__version__))
print("numpy version: {:s}".format(np.__version__))
print("pandas version: {:s}".format(pd.__version__))
print("scikit-learn version: {:s}".format(sklearn.__version__))
print("skm version: {:s}".format(skm.__version__))
print("")


# Load SKM model.
models_dir = localmodule.get_models_dir()
model_name = "skm-cv"
model_dir = os.path.join(models_dir, model_name)
unit_dir = os.path.join(model_dir, test_unit_str)
trial_str = "trial-" + str(trial_id)
trial_dir = os.path.join(unit_dir, trial_str)
skm_name = "_".join([
    dataset_name,
    model_name,
    test_unit_str,
    trial_str,
    "model.pkl"
])
skm_path = os.path.join(trial_dir, skm_name)
skm_model = skm.SKM(k=256)
skm_model = skm_model.load(skm_path)


# Load scaler.
scaler_name = "_".join([
    dataset_name,
    model_name,
    test_unit_str,
    trial_str,
    "scaler.pkl"
])
scaler_path = os.path.join(trial_dir, scaler_name)
scaler = joblib.load(scaler_path)


# Load SVM model.
val_metrics_name = "_".join([
    dataset_name,
    model_name,
    test_unit_str,
    trial_str,
    "svm-model",
    "val-metrics.csv"])
val_metrics_path = os.path.join(trial_dir, val_metrics_name)
val_metrics_df = pd.read_csv(val_metrics_path, header=None,
    names=[
        "Dataset",
        "Test unit",
        "Trial ID",
        "log2(C)",
        "Validation accuracy (%)"
    ])
log2Cs = np.array(val_metrics_df["log2(C)"])
best_log2C_id = np.argmax(val_metrics_df["Validation accuracy (%)"])
best_log2C = log2Cs[best_log2C_id]
if np.sign(best_log2C) >= 0:
    best_log2C_str = "+" + str(abs(best_log2C)).zfill(2)
else:
    best_log2C_str = "-" + str(abs(best_log2C)).zfill(2)
svm_name = "_".join([
    dataset_name,
    model_name,
    test_unit_str,
    trial_str,
    "svm-proba-model",
    "log2C-(" + best_log2C_str + ").pkl"
])
svm_path = os.path.join(trial_dir, svm_name)
svc = joblib.load(svm_path)


# Load features.
logmelspec_name = "_".join([dataset_name, "skm-full-logmelspec"])
logmelspec_dir = os.path.join(data_dir, logmelspec_name)
hdf5_path = os.path.join(logmelspec_dir, test_unit_str + ".hdf5")
lms_container = h5py.File(hdf5_path)
lms_group = lms_container["logmelspec"]


# Compute number of hops.
n_hops = int(lms_group.shape[1] / hop_length) - 1


# Create CSV file.
prediction_name = "_".join([
    dataset_name,
    model_name,
    "test-" + test_unit_str,
    trial_str,
    "predict-" + test_unit_str,
    "full-predictions"
])
prediction_path = os.path.join(trial_dir, prediction_name + ".csv")
csv_file = open(prediction_path, 'w')
csv_writer = csv.writer(csv_file, delimiter=',')


# Create CSV header.
csv_header = [
    "Dataset",
    "Model",
    "Test unit",
    "Prediction unit",
    "Timestamp",
    "Predicted probability"
]
csv_writer.writerow(csv_header)
csv_file.close()


# Loop over chunks.
n_chunks = int(n_hops / chunk_size) + 1
for chunk_id in range(n_chunks):


    # Initialize list of clips.
    Xs = []


    # Loop over clips.
    n_hops_in_chunk = min(chunk_size, n_hops - chunk_id * chunk_size)
    for hop_id in range(n_hops_in_chunk):

        # Load clip in full logmelspec data.
        clip_start = (chunk_id*chunk_size + hop_id) * hop_length
        clip_stop = clip_start + patch_width
        Xs.append(np.ravel(lms_group[:, clip_start:clip_stop]))


    # Vectorize clips.
    X = np.stack(Xs)


    # Transform with SKM.
    X = skm_model.transform(X.T).T


    # Scale.
    X = scaler.transform(X)


    # Predict.
    y_pred = svc.predict_proba(X)[:, 1]


    # Open CSV file.
    csv_file = open(prediction_path, 'a')
    csv_writer = csv.writer(csv_file, delimiter=',')


    # Loop over clips.
    for hop_id in range(n_hops_in_chunk):
        # Store prediction as DataFrame row.
        timestamp = (chunk_id*chunk_size + hop_id) * hop_duration
        timestamp_str = "{:9.3f}".format(timestamp)
        predicted_probability_str = "{:.16f}".format(y_pred[hop_id])
        row = [
            dataset_name,
            model_name,
            test_unit_str,
            test_unit_str,
            timestamp_str,
            predicted_probability_str]
        csv_writer.writerow(row)


    # Close CSV file.
    csv_file.close()



print(str(datetime.datetime.now()) + " Finish.")
elapsed_time = time.time() - int(start_time)
elapsed_hours = int(elapsed_time / (60 * 60))
elapsed_minutes = int((elapsed_time % (60 * 60)) / 60)
elapsed_seconds = elapsed_time % 60.
elapsed_str = "{:>02}:{:>02}:{:>05.2f}".format(elapsed_hours,
                                               elapsed_minutes,
                                               elapsed_seconds)
print("Total elapsed time: " + elapsed_str + ".")
