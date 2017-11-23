import h5py
import itertools
import numpy as np
import os
import pescador
import random


# This function implements the Bresenham's line algorithm in dimension one,
# in order to produce a list of pooling lengths of length n_layers such that
# np.prod(pool_list) * input_length = output_length
# These pooling lengths are chosen as powers of two, in such a way that
# the decrease in lengths between input_length and output_length is as
# progressive as possible.
# inspired by https://stackoverflow.com/a/19293966
def bresenham(input_length, output_length, n_layers):
    log2_total_pooling = np.floor(np.log2(input_length / output_length))
    floor_log2_pooling = int(np.floor(log2_total_pooling / n_layers))
    floor_pooling = 2**floor_log2_pooling
    ceil_log2_pooling = floor_log2_pooling + 1
    ceil_pooling = 2**ceil_log2_pooling

    n_floors = int(n_layers * ceil_log2_pooling - log2_total_pooling)
    n_ceils = n_layers - n_floors
    output_length * floor_pooling**n_floors * ceil_pooling**n_ceils

    floor_list = range(1, n_floors+1)
    ceil_list = range(-1, -n_ceils-1, -1)

    short_list, long_list = sorted((floor_list, ceil_list), key=len)
    n_shorts = len(short_list)
    n_longs = len(long_list)

    if long_list[0] > 0:
        short_pooling = ceil_pooling
        long_pooling = floor_pooling
    else:
        short_pooling = floor_pooling
        long_pooling = ceil_pooling

    if n_shorts == 0:
        pool_list = [long_pooling] * n_longs
    elif n_shorts == 1:
        prefix = [long_pooling] * int(np.floor(n_longs / 2))
        suffix = [long_pooling] * int(np.ceil(n_longs / 2))
        pool_list = prefix + [short_pooling] + suffix
    else:
        groups = itertools.groupby(
            ((long_list[n_longs*i//n_layers], short_list[n_shorts*i//n_layers])
              for i in range(n_layers)),
              key=lambda x:x[0])
        raw_list = [j[i] for k,g in groups for i,j in enumerate(g)]

        pool_list = []
        for n in raw_list:
            if n < 0:
                pool_list.append(ceil_pooling)
            else:
                pool_list.append(floor_pooling)


# We perform leave-one-unit-out cross-validation with 2 units for validation.
def fold_units():
    units = get_units()
    n_units = len(units)
    folds = []
    for fold_id in range(n_units):
        test_units = [units[fold_id]]
        train_units = []
        for unit_id in range(fold_id+1, fold_id+n_units-2):
            train_units.append(units[np.mod(unit_id, n_units)])
        val_units = [
            units[np.mod(fold_id-2, n_units)],
            units[np.mod(fold_id-1, n_units)]]
        folds.append([test_units, train_units, val_units])
    # TODO: assert that len(test_units)==1
    return folds


def get_augmentations():
    units = get_units()
    augmentations = {("noise-" + unit_str): 4 for unit_str in units}
    augmentations["original"] = 1
    augmentations["pitch"] = 4
    augmentations["stretch"] = 4
    return augmentations


def get_data_dir():
	return "/beegfs/vl1019/BirdVox-70k_data"


def get_dataset_name():
    return "BirdVox-70k"


def get_logmelspec_settings():
    logmelspec_settings = {
        "fmin": 2000,
        "fmax": 11025,
        "hop_length": 32,
        "n_fft": 1024,
        "n_mels": 128,
        "sr": 22050,
        "win_length": 256,
        "window": "hann"}
    return logmelspec_settings


def get_models_dir():
    return "/scratch/vl1019/BirdVox-70k_models"


def get_negative_labels():
    return ["alarm"]


def get_pcen_settings():
    pcen_settings = {
        "fmin": 2000,
        "fmax": 11025,
        "hop_length": 32,
        "n_fft": 1024,
        "n_mels": 128,
        "pcen_delta_denominator": 10,
        "pcen_time_constant_frames": 40,
        "pcen_norm_exponent": -0.8,
        "pcen_power": 0.25,
        "sr": 22050,
        "win_length": 256,
        "window": "hann"}
    return pcen_settings


def get_sample_rate():
    return 24000 # in Hertz


def get_tolerances():
    return np.arange(0.100, 0.550, 0.05) # in seconds


def get_units():
    return ["unit" + str(unit).zfill(2) for unit in [1, 2, 3, 5, 7, 10]]
    # TODO: assert that unit names do not contain underscores.


def multiplex_tfr(aug_kind_str, fold_units, n_hops, batch_size,
        tfr_str="logmelspec"):
    # Parse augmentation kind string (aug_kind_str).
    if aug_kind_str == "none":
        augs = ["original"]
    elif aug_kind_str == "pitch":
        augs = ["original", "pitch"]
    elif aug_kind_str == "stretch":
        augs = ["original", "stretch"]
    else:
        noise_augs = ["noise-" + unit_str for unit_str in fold_units]
        if aug_kind_str == "all":
            augs = noise_augs + ["original", "pitch", "stretch"]
        elif aug_kind_str == "noise":
            augs = noise_augs + ["original"]

    # Generate a Pescador streamer for every HDF5 container, that is,
    # every unit-augmentation-instance triplet.
    aug_dict = get_augmentations()
    data_dir = get_data_dir()
    dataset_name = get_dataset_name()
    tfr_name = "_".join([dataset_name, tfr_str])
    tfr_dir = os.path.join(data_dir, tfr_name)
    streams = []
    for aug_str in augs:
        aug_dir = os.path.join(tfr_dir, aug_str)
        if aug_str == "original":
            instances = [aug_str]
        else:
            n_instances = aug_dict[aug_str]
            instances = ["-".join([aug_str, str(instance_id)])
                for instance_id in range(n_instances)]
        if aug_str[:5] == "noise":
            bias = np.float32(-17.0)
        else:
            bias = np.float32(0.0)
        for instanced_aug_str in instances:
            for unit_str in fold_units:
                lms_name = "_".join([dataset_name, instanced_aug_str, unit_str])
                lms_path = os.path.join(aug_dir, lms_name + ".hdf5")
                stream = pescador.Streamer(yield_tfr,
                    lms_path, n_hops, bias, tfr_str)
                streams.append(stream)

    # Multiplex streamers together.
    mux = pescador.Mux(streams,
        k=len(streams), lam=None, with_replacement=True, revive=True)

    # Create buffered streamer with specified batch size.
    buffered_streamer = pescador.BufferedStreamer(mux, batch_size)

    return buffered_streamer.tuples("X", "y", cycle=True)



def pick_peaks(odf):
    derivative = np.diff(odf)
    pre_slope = np.insert(derivative, 0, -np.inf)
    post_slope = np.append(derivative, np.inf)
    peak_bools = np.logical_and((pre_slope > 0), (post_slope <= 0))
    locations = np.where(peak_bools)[0]
    return locations


def rsync():
    data_dir = get_data_dir()
    archive_dir = get_archive_dir()
    flags = ["-r"]
    command_words = ["rsync"] + flags + [data_dir, archive_dir]
    command_str = " ".join(command_words)
    os.command(command_str)


def yield_logmelspec(lms_path, n_hops, bias):
    # Open HDF5 container.
    with h5py.File(lms_path, "r") as lms_container:
        # Open HDF5 group corresponding to log-mel-spectrograms (lms).
        lms_group = lms_container["logmelspec"]

        # The naming convention of a key is
        # [unit]_[time]_[freq]_[y]_[aug]_[instance]
        # where y=1 if the key corresponds to a positive clip and 0 otherwise.
        keys = list(lms_group.keys())
        while True:
            # Pick a key uniformly as random.
            key = random.choice(keys)

            # Load logmelspec.
            X = lms_group[key]

            # Trim logmelspec in time to required number of hops.
            X_width = X.shape[1]
            first_col = int((X_width-n_hops) / 2)
            last_col = int((X_width+n_hops) / 2)
            X = X[:, first_col:last_col]

            # Add trailing singleton dimension for Keras interoperability.
            X = X[:, :, np.newaxis]

            # Apply bias
            X = X + bias

            # Retrieve label y from key name.
            y = np.array([np.float32(key.split("_")[3])])

            # Yield data and label as dictionary.
            yield dict(X=X, y=y)
