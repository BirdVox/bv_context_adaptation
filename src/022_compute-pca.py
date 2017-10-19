import datetime
import h5py
import librosa
import numpy as np
import os
import sklearn
import soundfile as sf
import sys
import time

import localmodule


# Define constants.
data_dir = localmodule.get_data_dir()
dataset_name = localmodule.get_dataset_name()
patch_width = 32
n_patches_per_clip = 3

# Parse arguments.
args = sys.argv[1:]
aug_str = args[0]
instance_id = int(args[1])
instance_str = str(instance_id)
test_unit_str = args[2]
if aug_str == "original":
    instanced_aug_str = aug_str
else:
    instanced_aug_str = "-".join([aug_str, instance_str])


# Retrieve fold such that test_unit_str is in the test set.
folds = localmodule.fold_units()
fold = [f for f in folds if test_unit_str in f[0]][0]
test_units = fold[0]
training_units = fold[1]
validation_units = fold[2]


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Computing PCA for " + dataset_name + " clips.")
print("Test Unit: " + test_unit_str + ".")
print("")
print("h5py version: {:s}".format(h5py.__version__))
print("librosa version: {:s}".format(librosa.__version__))
print("numpy version: {:s}".format(np.__version__))
print("scikit-learn version: {:s}".format(sklearn.__version__))
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




# Close HDF5 file.
in_file.close()


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
