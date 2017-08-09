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
augmentations = localmodule.get_augmentations()
dataset_name = localmodule.get_dataset_name()


# Read command-line arguments.
args = sys.argv[1:]
aug_kind_str = args[0]
unit_str = args[1]
trial_str = args[2]


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Training ICASSP convnet on " + dataset_name + ", " +
    unit_str, " trial " + trial_str + ".")
if aug_kind_str == "none":
    print("No data augmentation.")
elif aug_kind_str == "all":
    print("Data augmentation:")
    print()
else:
    print("")
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
