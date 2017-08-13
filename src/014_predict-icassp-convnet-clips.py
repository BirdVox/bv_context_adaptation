import datetime
import h5py
import keras
import numpy as np
import os
import pandas as pd
import pescador
import sys
import tensorflow as tf
import time

import localmodule


# Define constants.
dataset_name = localmodule.get_dataset_name()
folds = localmodule.fold_units()
models_dir = localmodule.get_models_dir()


# Read command-line arguments.
args = sys.argv[1:]
aug_kind_str = args[0]
test_unit_str = args[1]
trial_str = args[2]
predict_unit_str = args[3]


# Retrieve fold such that unit_str is in the test set.
fold = [f for f in folds if unit_str in f[0]][0]
test_units = fold[0]
training_units = fold[1]
validation_units = fold[2]


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Using Salamon's ICASSP 2017 convnet for binary classigification in " +
    dataset_name + ". ")
print("Training set: " + ", ".join(training_units) + ".")
print("Validation set: " + ", ".join(validation_units) + ".")
print("Test set: " + ", ".join(test_units) + ".")
print("")
print('h5py version: {:s}'.format(h5py.__version__))
print('keras version: {:s}'.format(keras.__version__))
print('numpy version: {:s}'.format(np.__version__))
print('pandas version: {:s}'.format(pd.__version__))
print('pescador version: {:s}'.format(pescador.__version__))
print('tensorflow version: {:s}'.format(tf.__version__))
print("")


# Load model.
model_name = "icassp-convnet"
if not aug_kind_str == "original":
    model_name = "_".join([model_name, aug_kind_str])
model_dir = os.path.join(models_dir, model_name)
unit_dir = os.path.join(model_dir, test_unit_str)
trial_dir = os.path.join(unit_dir, trial_str)
network_name = "_".join(
    [dataset_name, model_name, aug_kind_str,
     test_unit_str, trial_str, "network"])
network_path = os.path.join(trial_dir, network_name + ".hdf5")


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
