import datetime
import h5py
import librosa
import numpy as np
import os
import skm
import soundfile as sf
import sys
import time

import localmodule


# Define constants.
data_dir = localmodule.get_data_dir()
dataset_name = localmodule.get_dataset_name()
patch_width = 32
n_patches_per_clip = 10
aug_str = "original"
instanced_aug_str = aug_str


# Parse arguments.
args = sys.argv[1:]
test_unit_str = args[0]
trial_id = int(args[1])


# Retrieve fold such that test_unit_str is in the test set.
folds = localmodule.fold_units()
fold = [f for f in folds if test_unit_str in f[0]][0]
test_units = fold[0]
training_units = fold[1]
validation_units = fold[2]


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Training SKM for " + dataset_name + " clips.")
print("Test Unit: " + test_unit_str + ".")
print("Trial ID: " + str(trial_id) + ".")
print("")
print("h5py version: {:s}".format(h5py.__version__))
print("librosa version: {:s}".format(librosa.__version__))
print("numpy version: {:s}".format(np.__version__))
print("skm version: {:s}".format(skm.__version__))
print("")


# Define input folder.
logmelspec_name = "_".join([dataset_name, "skm-logmelspec"])
logmelspec_dir = os.path.join(data_dir, logmelspec_name)
aug_dir = os.path.join(logmelspec_dir, aug_str)


# Initialize matrix of training data.
X = []


# Loop over training units.
for train_unit_str in training_units:

    # Load HDF5 container of logmelspecs.
    hdf5_name = "_".join([dataset_name, instanced_aug_str, train_unit_str])
    in_path = os.path.join(aug_dir, hdf5_name + ".hdf5")
    in_file = h5py.File(in_path)


    # List clips.
    clip_names = list(in_file["logmelspec"].keys())


    # Loop over clips.
    for clip_name in clip_names:

        # Load logmelspec.
        logmelspec = in_file["logmelspec"][clip_name].value

        # Load time-frequency patches.
        logmelspec_width = logmelspec.shape[1]
        logmelspec_mid = np.round(logmelspec_width * 0.5).astype('int')
        logmelspec_start = logmelspec_mid -\
            np.round(patch_width * n_patches_per_clip * 0.5).astype('int')

        # Loop over time-frequency patches.
        for patch_id in range(n_patches_per_clip):

            # Extract patch.
            patch_start = logmelspec_start + patch_id * patch_width
            patch_stop = patch_start + patch_width
            patch = logmelspec[:, patch_start:patch_stop]

            # Ravel patch.
            X.append(np.ravel(patch))


# Concatenate raveled patches as rows and transpose.
X = np.stack(X).T


# Close HDF5 file.
in_file.close()


# Construct SKM model.
skm_model = skm.SKM(k=256)


# Train SKM.
skm_model.fit(X)


# Create folder for trial.
models_dir = localmodule.get_models_dir()
model_name = "skm-cv"
model_dir = os.path.join(models_dir, model_name)
os.makedirs(model_dir, exist_ok=True)
unit_dir = os.path.join(model_dir, test_unit_str)
os.makedirs(unit_dir, exist_ok=True)
trial_name = "trial-" + str(trial_id)
trial_dir = os.path.join(unit_dir, trial_name)
os.makedirs(trial_dir, exist_ok=True)


# Save SKM model.
model_name = "_".join([
    dataset_name, model_name, test_unit_str, trial_name, "model.pkl"
])
model_path = os.path.join(trial_dir, model_name)
skm_model.save(model_path)


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
