import csv
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
n_input_hops = 104
n_filters = [24, 48, 48]
kernel_size = [5, 5]
pool_size = [2, 4]
n_hidden_units = 64
steps_per_epoch = 256
validation_steps = 256
batch_size = 32
n_context_classes = 4


# Read command-line arguments.
args = sys.argv[1:]
aug_kind_str = "original"
bg_duration = int(args[0])
unit_str = args[1]


# Set number of epochs.
if aug_kind_str == "none":
    epochs = 16
else:
    epochs = 32


# Retrieve fold such that unit_str is in the test set.
fold = [f for f in folds if unit_str in f[0]][0]
test_units = fold[0]
training_units = fold[1]
validation_units = fold[2]


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Training Salamon's ICASSP 2017 convnet on " + dataset_name + ". ")
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


# Define and compile Keras model.
# NB: the original implementation of Justin Salamon in ICASSP 2017 relies on
# glorot_uniform initialization for all layers, and the optimizer is a
# stochastic gradient descent (SGD) with a fixed learning rate of 0.1.
# Instead, we use a he_normal initialization for the layers followed
# by rectified linear units (see He ICCV 2015), and replace the SGD by
# the Adam adaptive stochastic optimizer (see Kingma ICLR 2014).
# Moreover, we disable dropout because we found that it consistently prevented
# the model to train at all.

# Main channel.
# Input
spec_input = keras.layers.Input(
    shape=(128, n_input_hops, 1), name="spec_input")

# Layer 1
spec_bn = keras.layers.normalization.BatchNormalization(
    name="spec_bn")(spec_input)
spec_conv1 = keras.layers.Convolution2D(n_filters[0], kernel_size,
    padding="same", kernel_initializer="he_normal",
    name="spec_conv1")(spec_bn)
spec_pool1 = keras.layers.MaxPooling2D(
    pool_size=pool_size, name="spec_pool1")(spec_conv1)

# Layer 2
spec_conv2 = keras.layers.Convolution2D(n_filters[1], kernel_size,
    padding="same", kernel_initializer="he_normal",
    activation="relu", name="spec_conv2")(spec_pool1)
spec_pool2 = keras.layers.MaxPooling2D(
    pool_size=pool_size, name="spec_pool2")(spec_conv2)

# Layer 3
spec_conv3 = keras.layers.Convolution2D(n_filters[2], kernel_size,
    padding="same", kernel_initializer="he_normal",
    activation="relu", name="spec_conv3")(spec_pool2)

# Layer 4
spec_flatten = keras.layers.Flatten(
    name="spec_flatten")(spec_conv3)
spec_dense = keras.layers.Dense(n_hidden_units,
    kernel_initializer="he_normal", activation="relu",
    kernel_regularizer=keras.regularizers.l2(0.001),
    name="spec_dense1")(spec_flatten)

# Reshape.
spec_reshape = keras.layers.Reshape((-1, 4),
    name="spec_reshape")(spec_dense)


# Side channel.
# Input
bg_input = keras.layers.Input(
    shape=(128, 5), name="bg_input")

# Pool
bg_pool = keras.layers.AveragePooling1D(
    pool_size=4, name="bg_pool")(bg_input)

# Permute
bg_permute = keras.layers.Permute(
    (2, 1), name="bg_permute")(bg_pool)

# Conv
bg_conv = keras.layers.Conv1D(
    8, 1, kernel_initializer="he_normal",
    activation="relu", name="bg_conv")(bg_permute)

# Flatten
bg_flatten = keras.layers.Flatten(
    name="bg_flatten")(bg_conv)

# Dense 1
bg_dense1 = keras.layers.Dense(16,
    kernel_initializer="he_normal",
    activation="relu", name="bg_dense1")(bg_flatten)

# Dense 2
bg_dense2 = keras.layers.Dense(4,
    kernel_initializer="he_normal",
    activation="softmax", name="bg_dense2")(bg_dense1)

# Reshape
bg_reshape = keras.layers.Reshape((1, 4),
    name="bg_reshape")(bg_dense2)


# Element-wise multiplication
multiply = keras.layers.Multiply(
    name="multiply")([spec_reshape, bg_reshape])

# Flatten
flatten = keras.layers.Flatten(
    name="flatten")(multiply)


# Layer 5
# We put a single output instead of 43 in the original paper, because this
# is binary classification instead of multilabel classification.
# Furthermore, this layer contains 43 times less connections than in the
# original paper, so we divide the l2 weight penalization by 50, which is
# of the same order of magnitude as 43.
# 0.001 / 50 = 0.00002
dense = keras.layers.Dense(1,
    kernel_initializer="normal", activation="sigmoid",
    kernel_regularizer=keras.regularizers.l2(0.00002),
    name="dense")(flatten)


# Compile model, print model summary.
inputs = [spec_input, bg_input]
model = keras.models.Model(inputs=inputs, outputs=dense)
model.compile(loss="binary_crossentropy",
    optimizer="adam", metrics=["accuracy"])
model.summary()


# Build Pescador streamers corresponding to log-mel-spectrograms in augmented
# training and validation sets.
training_streamer = localmodule.multiplex_tfr(
    aug_kind_str, training_units, n_input_hops, batch_size)
validation_streamer = localmodule.multiplex_tfr(
    aug_kind_str, validation_units, n_input_hops, batch_size)


# Create directory for model, unit, and trial.
model_name = "icassp-convnet"
if not aug_kind_str == "none":
    model_name = "_".join([model_name, "aug-" + aug_kind_str])
model_dir = os.path.join(models_dir, model_name)
os.makedirs(model_dir, exist_ok=True)
unit_dir = os.path.join(model_dir, unit_str)
os.makedirs(unit_dir, exist_ok=True)
trial_dir = os.path.join(unit_dir, trial_str)
os.makedirs(trial_dir, exist_ok=True)


# Define Keras callback for checkpointing model.
network_name = "_".join(
    [dataset_name, model_name, unit_str, trial_str, "network"])
network_path = os.path.join(trial_dir, network_name + ".hdf5")
checkpoint = keras.callbacks.ModelCheckpoint(network_path,
    monitor="val_loss", verbose=False, save_best_only=True, mode="min")


# Define custom callback for saving history.
history_name = "_".join(
    [dataset_name, model_name, unit_str, trial_str, "history"])
history_path = os.path.join(trial_dir, history_name + ".csv")
with open(history_path, 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    header = [
        "Epoch", "Local time",
        "Training loss", "Training accuracy (%)",
        "Validation loss", "Validation accuracy (%)"]
    csv_writer.writerow(header)
def write_row(history_path, epoch, logs):
    with open(history_path, 'a') as csv_file:
        csv_writer = csv.writer(csv_file)
        row = [
            str(epoch).zfill(3),
            str(datetime.datetime.now()),
            "{:.16f}".format(logs.get('loss')),
            "{:.3f}".format(100*logs.get('acc')).rjust(7),
            "{:.16f}".format(logs.get('val_loss')),
            "{:.3f}".format(100*logs.get('val_acc')).rjust(7)]
        csv_writer.writerow(row)
history_callback = keras.callbacks.LambdaCallback(
    on_epoch_end=lambda epoch, logs: write_row(history_path, epoch, logs))


# Export network architecture as YAML file.
yaml_path = os.path.join(trial_dir, network_name + ".yaml")
with open(yaml_path, "w") as yaml_file:
    yaml_string = model.to_yaml()
    yaml_file.write(yaml_string)


# Train model.
history = model.fit_generator(
    training_streamer,
    steps_per_epoch = steps_per_epoch,
    epochs = epochs,
    verbose = False,
    callbacks = [checkpoint, history_callback],
    validation_data = validation_streamer,
    validation_steps = validation_steps)


# Print history.
history_df = pd.DataFrame(history.history)
print(history_df.to_string())
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
