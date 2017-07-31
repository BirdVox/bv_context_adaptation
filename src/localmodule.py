import itertools
import numpy as np
import os

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


# We perform leave-one-unit-out cross-validation with 2 units for validation
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
    return folds


def get_augmentations():
    units = get_units()
    augmentations = {("noise-" + unit_str): 4 for unit_str in units}
    augmentations["original"] = 1
    augmentations["pitch"] = 4
    augmentations["stretch"] = 4
    return augmentations


def get_archive_dir():
    return "/archive/vl1019/spl2017_data"


def get_data_dir():
	return "/beegfs/vl1019/spl2017_data"


def get_dataset_name():
    return "BirdVox-70k"


def get_models_dir():
    return "/scratch/vl1019/spl2017_models"


def get_negative_labels():
    return ["alarm"]


def get_sample_rate():
    return 24000 # in Hertz


def get_units():
    return ["unit" + str(unit).zfill(2) for unit in [1, 2, 3, 5, 7, 10]]


def pick_peaks(odf):
    derivative = np.diff([x])
    pre_slope = np.insert(derivative, 0, -np.inf)
    post_slope = np.append(derivative, np.inf)
    peak_bools = np.logical_and((pre_slope > 0), (post_slope < 0))
    locations = np.where(peak_bools)[0]
    return locations


def rsync():
    data_dir = get_data_dir()
    archive_dir = get_archive_dir()
    flags = ["-r"]
    command_words = ["rsync"] + flags + [data_dir, archive_dir]
    command_str = " ".join(command_words)
    os.command(command_str)
