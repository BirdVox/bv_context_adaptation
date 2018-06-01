import csv
import datetime
import h5py
import keras
import numpy as np
import os
import pandas as pd
import pescador
import pescador.maps
import random
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
bg_duration = 1800


# Read command-line arguments.
args = sys.argv[1:]
aug_kind_str = args[0]
unit_str = args[1]
trial_id = args[2]
trial_str = "trial-" + str(trial_id)


# Set number of epochs.
if aug_kind_str == "none":
    epochs = 64
else:
    epochs = 128


# Retrieve fold such that unit_str is in the test set.
fold = [f for f in folds if unit_str in f[0]][0]
test_units = fold[0]
training_units = fold[1]
validation_units = fold[2]


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Training deep context adaptation on " +\
    dataset_name + " with PCEN input. ")
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


# Define function for multiplexing streamers.
def multiplex_lms_with_background(
        aug_kind_str, fold_units, n_input_hops, batch_size):

    # Define constants.
    aug_dict = localmodule.get_augmentations()
    data_dir = localmodule.get_data_dir()
    dataset_name = localmodule.get_dataset_name()
    tfr_name = "_".join([dataset_name, "clip-pcen"])
    tfr_dir = os.path.join(data_dir, tfr_name)
    bg_name = "_".join(
        [dataset_name, "clip-pcen-backgrounds"])
    bg_dir = os.path.join(data_dir, bg_name)
    T_str = "T-" + str(bg_duration).zfill(4)
    T_dir = os.path.join(bg_dir, T_str)

    # Parse augmentation kind string (aug_kind_str).
    if aug_kind_str == "none":
        augs = ["original"]
    elif aug_kind_str == "pitch":
        augs = ["original", "pitch"]
    elif aug_kind_str == "stretch":
        augs = ["original", "stretch"]
    elif aug_kind_str == "all-but-noise":
        augs = ["original", "pitch", "stretch"]
    else:
        noise_augs = ["noise-" + unit_str for unit_str in fold_units]
        if aug_kind_str == "all":
            augs = noise_augs + ["original", "pitch", "stretch"]
        elif aug_kind_str == "noise":
            augs = noise_augs + ["original"]

    # Loop over augmentations.
    streams = []
    for aug_str in augs:

        # Define instances.
        aug_dir = os.path.join(tfr_dir, aug_str)
        if aug_str == "original":
            instances = [aug_str]
        else:
            n_instances = aug_dict[aug_str]
            instances = ["-".join([aug_str, str(instance_id)])
                for instance_id in range(n_instances)]

        # Loop over instances.
        for instanced_aug_str in instances:

            # Loop over units.
            for unit_str in fold_units:

                # Define path to time-frequency representation.
                lms_name = "_".join(
                    [dataset_name, instanced_aug_str, unit_str])
                lms_path = os.path.join(aug_dir, lms_name + ".hdf5")

                # Define path to background.
                bg_name = "_".join(
                    [dataset_name, "clip-backgrounds",
                     unit_str, T_str + ".hdf5"])
                bg_path = os.path.join(T_dir, bg_name)

                # Define pescador streamer.
                bias = 0.0
                stream = pescador.Streamer(yield_lms_and_background,
                    lms_path, n_input_hops, bias, bg_path)
                streams.append(stream)

    # Multiplex streamers together.
    mux = pescador.Mux(streams,
        k=len(streams), lam=None, with_replacement=True, revive=True)

    # Create buffered streamer with specified batch size.
    buffered_streamer = pescador.BufferedStreamer(mux, batch_size)

    return pescador.maps.keras_tuples(buffered_streamer,
        inputs=["X_spec", "X_bg"], outputs=["y"])


# Define function for yielding logmelspec (lms) and background.
def yield_lms_and_background(tfr_path, n_input_hops, bias, bg_path):

    # Open HDF5 containers for TFR and background.
    with h5py.File(tfr_path, "r") as tfr_container,\
            h5py.File(bg_path, "r") as bg_container:
        # Open HDF5 group corresponding to time-freq representation (TFR).
        tfr_group = tfr_container["pcen"]

        # The naming convention of a key is
        # [unit]_[time]_[freq]_[y]_[aug]_[instance]
        # where y=1 if the key corresponds to a positive clip and 0 otherwise.
        keys = list(tfr_group.keys())

        # Open HDF5 group corresponding to background
        bg_group = bg_container["pcen_background"]

        # Infinite "yield" loop.
        while True:
            # Pick a key uniformly as random.
            key = random.choice(keys)

            # Load time-frequency spectrogram (TFR).
            X_spec = tfr_group[key]

            # Trim TFR in time to required number of hops.
            X_width = X_spec.shape[1]
            first_col = int((X_width-n_input_hops) / 2)
            last_col = int((X_width+n_input_hops) / 2)
            X_spec = X_spec[:, first_col:last_col]

            # Add trailing singleton dimension for Keras interoperability.
            X_spec = X_spec[:, :, np.newaxis]

            # Apply bias
            X_spec = X_spec + bias

            # Load background.
            bg_key = "_".join(key.split("_")[:4])
            X_bg = bg_group[bg_key]
            X_bg = np.transpose(X_bg)

            # Retrieve label y from key name.
            # We permute labels 0.0 and 1.0 because we need
            # a better floating-point precision for positive samples
            # than for negative samples.
            y = np.array([1.0 - np.float32(key.split("_")[3])])

            # Yield data and label as dictionary.
            yield dict(X_spec=X_spec, X_bg=X_bg, y=y)


# Define and compile Keras model.
# Spectrogram channel.
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
spec_pool3 = keras.layers.MaxPooling2D(
    pool_size=pool_size, name="spec_pool3")(spec_conv3)

# Layer 4
spec_conv4 = keras.layers.Convolution2D(n_filters[3], kernel_size,
    padding="same", kernel_initializer="he_normal",
    activation="relu", name="spec_conv4")(spec_pool3)
spec_pool4 = keras.layers.MaxPooling2D(
    pool_size=pool_size, name="spec_pool4")(spec_conv4)

# Layer 4
spec_reshape = keras.layers.Reshape((-1, 8),
    name="spec_reshape")(spec_pool4)


# Background channel.
# Input
bg_input = keras.layers.Input(
    shape=(128, 9), name="bg_input")

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

# Weights (mixture of experts)
bg_experts = keras.layers.Dense(8,
    kernel_initializer="he_normal",
    activation="tanh",
    name="bg_experts")(bg_flatten)

# Transposed weights
bg_transposed = keras.layers.Reshape((1, 8),
    name="bg_transposed")(bg_experts)

# Bias (adaptive threshold)
bg_bias = keras.layers.Dense(1,
    name="adaptive_threshold", use_bias=False)(bg_flatten)


# Combined channel.
# Element-wise multiplication
multiply = keras.layers.Multiply(
    name="multiply")([spec_reshape, bg_transposed])

# Transpose
multiply_transposed = keras.layers.Permute((2, 1),
    name="multiply_transposed")(multiply)

# Dense layer with weight sharing across eperts
dense_across_experts = keras.layers.Dense(64,
    activation="relu",
    name="dense_across_experts")(multiply_transposed)

# Transpose again
dense_across_experts_transposed = keras.layers.Permute((2, 1),
    name="dense_across_experts_transposed")(dense_across_experts)

# Mixture of experts
mixture_of_experts = keras.layers.Lambda(lambda x: K.sum(x, axis=2),
    name="mixture_of_experts")(dense_across_experts_transposed)

# Dropout
dropout = keras.layers.Dropout(0.5)(dropout)

# Event detection function
edf = keras.layers.Dense(1, activation="sigmoid", name="edf")(dropout)


# Build Pescador streamers corresponding to log-mel-spectrograms in augmented
# training and validation sets.
training_streamer = multiplex_lms_with_background(
    aug_kind_str, training_units, n_input_hops, batch_size)
validation_streamer = multiplex_lms_with_background(
    aug_kind_str, validation_units, n_input_hops, batch_size)


# Create directory for model, unit, and trial.
model_name = "pcen-deepcontext"
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


# Rejection sampling for best initialization.
n_inits = 10
inputs = [spec_input, bg_input]
for init_id in range(n_inits):
    model = keras.models.Model(inputs=inputs, outputs=dense)
    model.compile(loss="binary_crossentropy",
        optimizer="adam", metrics=["accuracy"])
    history = model.fit_generator(
        training_streamer,
        steps_per_epoch = steps_per_epoch,
        epochs = 4,
        verbose = False,
        callbacks = [history_callback],
        validation_data = validation_streamer,
        validation_steps = validation_steps)
    history_df = pd.read_csv(history_path)
    val_acc = 100 * list(history_df["Validation accuracy (%)"])[-1]
    if val_acc > 60.0:
        break


# Export network architecture as YAML file.
yaml_path = os.path.join(trial_dir, network_name + ".yaml")
with open(yaml_path, "w") as yaml_file:
    yaml_string = model.to_yaml()
    yaml_file.write(yaml_string)


# Print model summary.
model.summary()


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
