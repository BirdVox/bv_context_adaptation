import datetime
import h5py
import keras
import numpy as np
import os
import pescador
import tensorflow as tf
import time
import sys

import localmodule


# Define constants.
dataset_name = localmodule.get_dataset_name()
folds = localmodule.fold_units()
n_input_hops = 104
n_filters = [24, 48, 48]
kernel_size = [5, 5]
pool_size = [2, 4]
n_hidden_units = 64


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


# Define and compile Keras model.
model = keras.models.Sequential()

# Layer 1
bn = keras.layers.normalization.BatchNormalization(
    input_shape=(128, n_input_hops, 1))
model.add(bn)
conv1 = keras.layers.Convolution2D(n_filters[0], kernel_size,
    padding="same", kernel_initializer="he_normal", activation="relu")
model.add(conv1)
pool1 = keras.layers.MaxPooling2D(pool_size=pool_size)
model.add(pool1)

# Layer 2
conv2 = keras.layers.Convolution2D(n_filters[1], kernel_size,
    padding="same", kernel_initializer="he_normal", activation="relu")
model.add(conv2)
pool2 = keras.layers.MaxPooling2D(pool_size=pool_size)
model.add(pool2)

# Layer 3
conv3 = keras.layers.Convolution2D(n_filters[2], kernel_size,
    padding="same", kernel_initializer="he_normal", activation="relu")
model.add(conv3)

# Layer 4
drop1 = keras.layers.Dropout(0.5)
model.add(drop1)
flatten = keras.layers.Flatten()
model.add(flatten)
dense1 = keras.layers.Dense(n_hidden_units,
    kernel_initializer="he_normal", activation="relu")
model.add(dense1)

# Layer 5
# We put a single output instead of 43 in the original paper, because this
# is binary classification instead of multilabel classification.
drop2 = keras.layers.Dropout(0.5)
model.add(drop2)
dense2 = keras.layers.Dense(1,
    kernel_initializer="glorot_uniform", activation="softmax")
model.add(dense2)


# Print model summary.
model.summary()


# Multiplex




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
