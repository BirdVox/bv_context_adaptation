import h5py
import os

# Define constants.
data_dir = localmodule.get_data_dir()
BirdVox_wav_dir = os.path.join(data_dir, "BirdVox-70k_wav")
units = localmodule.get_units()
augmentations = localmodule.get_augmentations()


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start")
print("Saving BirdVox-70k data into HDF5 containers.")
print("h5py version: {:s}'.format(h5py.__version__)")
print("")

# Loop over augmentations.
for aug_str in augmentations:
    n_instances = augmentations[aug_str]

    # Loop over instances.
    for instance_id in range(n_instances):
        instance_str = str(instance_id)
        instanced_aug_str = "-".join(aug_str, instance_str)
        instanced_aug_dir = os.path.join(BirdVox_wav_dir, instanced_aug_str)

        # Loop over recording units.
        for unit in units:
            unit_str = "unit" + str(unit).zfill(2)
            in_unit_dir = os.path.join(instanced_aug_dir, unit_str)
