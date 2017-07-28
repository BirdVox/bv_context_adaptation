import os


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


def rsync():
    data_dir = get_data_dir()
    archive_dir = get_archive_dir()
    flags = ["-r"]
    command_words = ["rsync"] + flags + [data_dir, archive_dir]
    command_str = " ".join(command_words)
    os.command(command_str)


# We perform leave-one-unit-out cross-validation with 2 units for validation
def split_units():
    units = localmodule.get_units()
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
