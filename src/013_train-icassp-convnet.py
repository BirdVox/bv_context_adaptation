import datetime
import h5py
import keras
import numpy as np
import os
import tensorflow as tf
import time
import sys

import localmodule


# Define constants.
aug_dict = localmodule.get_augmentations()
dataset_name = localmodule.get_dataset_name()
folds = localmodule.fold_units()


# Read command-line arguments.
args = sys.argv[1:]
aug_kind_str = args[0]
unit_str = args[1]
trial_str = args[2]


# Retrieve fold such that unit_str is in the test set.
fold = [f for f in folds if unit_str in f[0]][0]
test_units = fold[0]
training_units = fold[1]
val_units = fold[2]


# Get training augmentations and validation augmentations as string keywords.
training_augs, val_augs = \
    localmodule.parse_augmentation_kind(aug_kind_str, training_units, val_units)


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Training Salamon's ICASSP 2017 convnet on " + dataset_name + ". ")
print("Training set: " + ", ".join(training_units) + ".")
print("Validation set: " + ", ".join(val_units) + ".")
print("Test set: " + ", ".join(test_units) + ".")
print("")
print("Training augmentations: " + ", ".join(training_augs) + ".")
print("Validation augmentations: " + ", ".join(validation_augs) + ".")
print("")
print('h5py version: {:s}'.format(h5py.__version__))
print('keras version: {:s}'.format(keras.__version__))
print('numpy version: {:s}'.format(np.__version__))
print('pescador version: {:s}'.format(pescador.__version__))
print('tensorflow version: {:s}'.format(tf.__version__))
print("")


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
