import csv
import datetime
from sklearn.externals import joblib
import numpy as np
import os
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
log2Cs = range(-5, 15)


# Parse arguments.
args = ["unit01", "0"]
test_unit_str = args[0]
trial_id = int(args[1])


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Training SVM for " + dataset_name + " clips.")
print("Test unit: " + test_unit_str + ".")
print("Trial ID: " + str(trial_id) + ".")
print("")
print("numpy version: {:s}".format(np.__version__))
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
    for clip_name in clip_names[:10]: #UPDATE
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


# Define in-place standardizer.
scaler = sklearn.preprocessing.StandardScaler(copy=False)


# Standardize training set.
scaler.fit_transform(X_train)


# Save scaler.
scaler_name = "_".join([
    dataset_name,
    "skm-cv",
    test_unit_str,
    trial_str,
    "scaler.pkl"
])
scaler_path = os.path.join(trial_dir, scaler_name)
joblib.dump(scaler, scaler_path);


# Initialize matrix of validation data..
X_val = []
y_val = []


# Loop over validation units.
for val_unit_str in validation_units:

    # Load HDF5 container of logmelspecs.
    hdf5_name = "_".join([dataset_name, instanced_aug_str, val_unit_str])
    in_path = os.path.join(aug_dir, hdf5_name + ".hdf5")
    in_file = h5py.File(in_path)


    # List clips.
    clip_names = list(in_file["logmelspec"].keys())


    # Loop over clips.
    for clip_name in clip_names:
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

        # Append X and y.
        X_val.append(np.ravel(patch))
        y_val.append(y_clip)


# Concatenate raveled patches as rows and transpose.
X_val = np.stack(X_val)


# Transform training set.
X_val = skm_model.transform(X_val.T).T


# Scale validation data.
X_val = scaler.transform(X_val)


# Define CSV file for validation metrics.
val_metrics_name = "_".join([
    dataset_name,
    "skm-cv",
    test_unit_str,
    trial_str,
    "svm-model",
    "val-metrics.csv"
])
val_metrics_path = os.path.join(
    trial_dir, val_metrics_name)


# Open CSV file.
csv_file = open(val_metrics_path, 'w')
csv_writer = csv.writer(csv_file, delimiter=',')
csv_header = [
    "Dataset",
    "Test unit",
    "Trial ID",
    "log2(C)",
    "Validation accuracy (%)"
]
csv_writer.writerow(csv_header)


# Loop over C (regularization parameter).
val_accs = []
for log2C in log2Cs:

    # Define SVM.
    svc = sklearn.svm.SVC(
        C=2.0**log2C,
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

    # Train classifier.
    svc.fit(X_train, y_train)

    # Save model.
    if np.sign(log2C) >= 0:
        log2C_str = "+" + str(abs(log2C)).zfill(2)
    else:
        log2C_str = "-" + str(abs(log2C)).zfill(2)
    svm_name = "_".join([
        dataset_name,
        "skm-cv",
        test_unit_str,
        trial_str,
        "svm-model",
        "log2C-(" + log2C_str + ").pkl"
    ])
    svm_path = os.path.join(trial_dir, svm_name)
    joblib.dump(svc, svm_path)

    # Print validation score.
    val_acc = svc.score(X_val, y_val)
    val_accs.append(val_acc)
    print("C = {:14.6f}; acc = {:5.2f}%".format(2.0**log2C, 100*val_acc))

    # Write row.
    row = [
    dataset_name,
    test_unit_str,
    str(trial_id),
    log2C_str,
    "{:5.2f}".format(100*val_acc)
    ]
    csv_writer.writerow(row)


# Close CSV file.
csv_file.close()


# Compute best C.
val_accs = np.array(val_accs)
best_acc = np.max(val_accs)
best_log2C = log2Cs[np.argmax(val_accs)]


# Print best C.
print("")
print("Best: C = {:10.6f}; acc = {:5.2f}%".format(
    2.0**best_log2C, 100*best_acc))


# Load best model.
if np.sign(log2C) >= 0:
    best_log2C_str = "+" + str(abs(best_log2C)).zfill(2)
else:
    best_log2C_str = "-" + str(abs(best_log2C)).zfill(2)
svm_name = "_".join([
    dataset_name,
    "skm-cv",
    test_unit_str,
    trial_str,
    "svm-model",
    "log2C-(" + best_log2C_str + ").pkl"
])
svm_path = os.path.join(trial_dir, svm_name)
best_svc = joblib.load(svm_path)


# Define CSV file for validation metrics.
val_predictions_name = "_".join([
    dataset_name,
    "skm-cv",
    test_unit_str,
    trial_str,
    "svm-model",
    "val-predictions.csv"
])
val_predictions_path = os.path.join(
    trial_dir, val_predictions_name)


# Predict on validation data.
csv_file = open(val_predictions_path, 'w')
csv_writer = csv.writer(csv_file, delimiter=',')
csv_header = [
    "Dataset",
    "Test unit",
    "Trial ID",
    "log2(C)",
    "Prediction unit",
    "Clip name",
    "Ground truth",
    "Log probaility"
]
csv_writer.writerow(csv_header)


# Loop over validation units.
for val_unit_str in validation_units:

    # Initialize X and y for given validation unit.
    X_val = []
    y_val = []


    # Load HDF5 container of logmelspecs.
    hdf5_name = "_".join([dataset_name, instanced_aug_str, val_unit_str])
    in_path = os.path.join(aug_dir, hdf5_name + ".hdf5")
    in_file = h5py.File(in_path)


    # List clips.
    clip_names = list(in_file["logmelspec"].keys())
    clip_names = sorted(clip_names)


    # Loop over clips.
    for clip_name in clip_names:
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
        patch = np.ravel(patch)

        X_val.append(patch)
        y_val.append(y_clip)


    # Concatenate raveled patches as rows and transpose.
    X_val = np.stack(X_val)


    # Transform validation data.
    X_val = skm_model.transform(X_val.T).T


    # Scale validation data.
    X_val = scaler.transform(X_val)


    # Predict.
    y_val_predicted = svc.predict_log_proba(X_val)[:, 1]


    # Loop over clips.
    for clip_id, clip_name in enumerate(clip_names):
        # Write row.
        row = [
            dataset_name,
            test_unit_str,
            str(trial_id),
            log2C_str,
            val_unit_str,
            "{:17.12f}".format(y_val_predicted[clip_id])]
        csv_writer.writerow(row)

# Close CSV file.
csv_file.close()


# Define CSV file for test metrics.
test_predictions_name = "_".join([
    dataset_name,
    "skm-cv",
    test_unit_str,
    trial_str,
    "svm-model",
    "test-predictions.csv"
])
test_predictions_path = os.path.join(
    trial_dir, test_predictions_name)


# Predict on validation data.
csv_file = open(test_predictions_path, 'w')
csv_writer = csv.writer(csv_file, delimiter=',')
csv_header = [
    "Dataset",
    "Test unit",
    "Trial ID",
    "log2(C)",
    "Prediction unit",
    "Clip name",
    "Ground truth",
    "Log probaility"
]
csv_writer.writerow(csv_header)


# Initialize X and y for given validation unit.
X_test = []
y_test = []


# Load HDF5 container of logmelspecs.
hdf5_name = "_".join([dataset_name, instanced_aug_str, test_unit_str])
in_path = os.path.join(aug_dir, hdf5_name + ".hdf5")
in_file = h5py.File(in_path)


# List clips.
clip_names = list(in_file["logmelspec"].keys())
clip_names = sorted(clip_names)


# Loop over clips.
for clip_name in clip_names:
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
    patch = np.ravel(patch)

    X_test.append(patch)
    y_test.append(y_clip)


# Concatenate raveled patches as rows and transpose.
X_test = np.stack(X_test)


# Transform validation data.
X_test = skm_model.transform(X_test.T).T


# Scale validation data.
X_test = scaler.transform(X_test)


# Predict.
y_test_predicted = svc.predict_log_proba(X_test)[:, 1]


# Loop over clips.
for clip_id, clip_name in enumerate(clip_names):
    # Write row.
    row = [
        dataset_name,
        test_unit_str,
        str(trial_id),
        log2C_str,
        test_unit_str,
        "{:17.12f}".format(y_test_predicted[clip_id])]
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
