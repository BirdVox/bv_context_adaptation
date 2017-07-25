def get_augmentations():
    units = get_units()
    augmentations = {("noise-unit"+str(unit).zfill(2)): 4 for unit in units}
    augmentations["original"] = 1
    augmentations["pitch"] = 4
    augmentations["stretch"] = 4
    return augmentations


def get_data_dir():
	return "/scratch/vl1019/spl2017_data"


def get_units():
    return [1, 2, 3, 5, 7, 10]
