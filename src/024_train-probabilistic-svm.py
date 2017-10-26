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


# Parse arguments.
args = sys.argv[1:]
test_unit_str = args[0]
trial_id = int(args[1])


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Training probabilistic SVM for " + dataset_name + " clips.")
print("Test unit: " + test_unit_str + ".")
print("Trial ID: " + str(trial_id) + ".")
print("")
print("h5py version: {:s}".format(h5py.__version__))
print("numpy version: {:s}".format(np.__version__))
print("pandas version: {:s}".format(pd.__version__))
print("scikit-learn version: {:s}".format(sklearn.__version__))
print("skm version: {:s}".format(skm.__version__))
print("")


# Retrieve fold such that test_unit_str is in the test set.
folds = localmodule.fold_units()
fold = [f for f in folds if test_unit_str in f[0]][0]
test_units = fold[0]
training_units = fold[1]
validation_units = fold[2]


# Define input folder.
logmelspec_name = "_".join([dataset_name, "skm-logmelspec"])
logmelspec_dir = os.path.join(data_dir, logmelspec_name)
aug_dir = os.path.join(logmelspec_dir, aug_str)


# Initialize matrix of training data.
X_train = []
y_train = []


# Loop over training units.
for train_unit_str in training_units:

    # Load HDF5 container of logmelspecs.
    hdf5_name = "_".join([dataset_name, instanced_aug_str, train_unit_str])
    in_path = os.path.join(aug_dir, hdf5_name + ".hdf5")
    in_file = h5py.File(in_path)


    # List clips.
    clip_names = list(in_file["logmelspec"].keys())


    # Loop over clips.
    for clip_name in clip_names[:100]:
        # Read label.
        y_clip = int(clip_name.split("_")[3])

        # Load logmelspec.
        logmelspec = in_file["logmelspec"][clip_name].value

        # Load time-frequency patches.
        logmelspec_width = logmelspec.shape[1]
        logmelspec_mid = np.round(logmelspec_width * 0.5).astype('int')
        logmelspec_start = logmelspec_mid -\
            np.round(patch_width * n_patches_per_clip * 0.5).astype('int')

        # Extract patch.
        patch_start = logmelspec_start
        patch_stop = patch_start + patch_width
        patch = logmelspec[:, patch_start:patch_stop]

        # Ravel patch.
        X_train.append(np.ravel(patch))

        # Append label.
        y_train.append(y_clip)


# Concatenate raveled patches as rows.
X_train = np.stack(X_train)


# Load SKM model.
models_dir = localmodule.get_models_dir()
model_name = "skm-cv"
model_dir = os.path.join(models_dir, model_name)
unit_dir = os.path.join(model_dir, test_unit_str)
trial_str = "trial-" + str(trial_id)
trial_dir = os.path.join(unit_dir, trial_str)
model_name = "_".join([
    dataset_name, model_name, test_unit_str, trial_str, "model.pkl"
])
model_path = os.path.join(trial_dir, model_name)
skm_model = skm.SKM(k=256)
skm_model = skm_model.load(model_path)


# Transform training set with SKM.
X_train = skm_model.transform(X_train.T).T


# Load standardizer.
scaler_name = "_".join([
    dataset_name,
    "skm-cv",
    test_unit_str,
    trial_str,
    "scaler.pkl"
])
scaler_path = os.path.join(trial_dir, scaler_name)
scaler = joblib.load(scaler_path)


# Standardize training set.
X_train = scaler.transform(X_train)


# Define CSV file for validation metrics.
val_metrics_name = "_".join([
    dataset_name,
    "skm-cv",
    test_unit_str,
    trial_str,
    "svm-model",
    "val-metrics.csv"
])
csv_header = [
    "Dataset",
    "Test unit",
    "Trial ID",
    "log2(C)",
    "Validation accuracy (%)"
]
val_metrics_path = os.path.join(
    trial_dir, val_metrics_name)


# Open CSV file as Pandas DataFrame.
val_metrics_df = pd.read_csv(val_metrics_path, header=None, names=csv_header)


# Find C maximizing validation accuracy.
max_val_acc = np.max(val_metrics_df["Validation accuracy (%)"])
best_log2C = val_metrics_df["log2(C)"][np.argmax(val_metrics_df["Validation accuracy (%)"])]


# Define SVM model.
svc = sklearn.svm.SVC(
    C=2.0**best_log2C,
    kernel='rbf',
    degree=3,
    gamma='auto',
    coef0=0.0,
    shrinking=True,
    probability=True,
    tol=0.001,
    cache_size=200,
    class_weight=None,
    verbose=False,
    max_iter=-1,
    random_state=None)


# Train SVM model.
svc.fit(X_train, y_train)


# Save SVM model.
if np.sign(best_log2C) >= 0:
    best_log2C_str = "+" + str(abs(best_log2C)).zfill(2)
else:
    best_log2C_str = "-" + str(abs(best_log2C)).zfill(2)
svm_name = "_".join([
    dataset_name,
    "skm-cv",
    test_unit_str,
    trial_str,
    "svm-proba-model",
    "log2C-(" + best_log2C_str + ").pkl"
])
svm_path = os.path.join(trial_dir, svm_name)
joblib.dump(svc, svm_path)


# Initialize matrix of test data.
X_test = []
y_test = []


# Load HDF5 container of logmelspecs.
hdf5_name = "_".join([dataset_name, instanced_aug_str, test_unit_str])
in_path = os.path.join(aug_dir, hdf5_name + ".hdf5")
in_file = h5py.File(in_path)


# List clips.
clip_names = list(in_file["logmelspec"].keys())


# Loop over clips.
for clip_name in clip_names[:100]:
    # Read label.
    y_clip = int(clip_name.split("_")[3])

    # Load logmelspec.
    logmelspec = in_file["logmelspec"][clip_name].value

    # Load time-frequency patches.
    logmelspec_width = logmelspec.shape[1]
    logmelspec_mid = np.round(logmelspec_width * 0.5).astype('int')
    logmelspec_start = logmelspec_mid -\
        np.round(patch_width * n_patches_per_clip * 0.5).astype('int')

    # Extract patch.
    patch_start = logmelspec_start
    patch_stop = patch_start + patch_width
    patch = logmelspec[:, patch_start:patch_stop]

    # Ravel patch.
    X_test.append(np.ravel(patch))

    # Append label.
    y_test.append(y_clip)


# Concatenate raveled patches as rows.
X_test = np.stack(X_test)


# Transform test set with SKM.
X_test = skm_model.transform(X_test.T).T


# Standardize test set.
X_test = scaler.transform(X_test)


# Predict.
y_test = svc.predict(X_test)


# Create CSV file.
model_name = "skm-proba"
predict_unit_str = test_unit_str
prediction_name = "_".join([dataset_name, model_name,
    "test-" + test_unit_str, trial_str, "predict-" + predict_unit_str,
    "clip-predictions"])
prediction_path = os.path.join(trial_dir, prediction_name + ".csv")
csv_file = open(prediction_path, 'w')
csv_writer = csv.writer(csv_file, delimiter=',')


# Create CSV header.
csv_header = ["Dataset", "Test unit", "Prediction unit", "Timestamp",
    "Key", "Predicted probability"]
csv_writer.writerow(csv_header)


# Loop over keys.
for clip_id, key in clip_names:
    # Store prediction as DataFrame row.
    key_split = key.split("_")
    timestamp_str = key_split[1]
    freq_str = key_split[2]
    ground_truth_str = key_split[3]
    aug_str = key_split[4]
    predicted_probability = y_test[clip_id]
    predicted_probability_str = "{:.16f}".format(predicted_probability)
    row = [dataset_name, test_unit_str, predict_unit_str, timestamp_str,
         freq_str, aug_str, key, ground_truth_str, predicted_probability_str]
    csv_writer.writerow(row)


# Close HDF5 containers.
lms_container.close()


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
