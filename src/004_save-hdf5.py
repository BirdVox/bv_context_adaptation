import h5py
import os
import pandas as pd

# Define constants.
data_dir = localmodule.get_data_dir()
dataset_name = localmodule.get_dataset_name()
dataset_wav_name = "_".join([dataset_name, "audio-clips"])
dataset_wav_dir = os.path.join(data_dir, dataset_wav_name)
units = localmodule.get_units()
augmentations = localmodule.get_augmentations()


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Saving " + dataset_name + " audio data and metadata into HDF5 containers.")
print("h5py version: {:s}.".format(h5py.__version__))
print("pandas version: {:s}.".format(pd.__version__))
print("")


# Create directory for HDF5 data.
dataset_hdf5_name = "_".join([dataset_name, "hdf5"])
dataset_hdf5_dir = os.path.join(datadir, dataset_hdf5_name)
if not os.path.exists(dataset_hdf5_dir):
    os.makedirs(dataset_hdf5_dir)


# Load GPS coordinates as Pandas dataframe.
gps_name = "_".join([dataset_name, "gps-coordinates"])
gps_path = os.path.join(data_dir, gps_name)
gps_df = pd.read_csv(gps_path)


# Loop over augmentations.
for aug_str in augmentations:
    n_instances = augmentations[aug_str]

    # Loop over instances.
    for instance_id in range(n_instances):
        # Define directory for instanced augmentation.
        if aug_str == "original":
            instanced_aug_str = aug_str
        else:
            instance_str = str(instance_id)
            instanced_aug_str = "_".join(aug_str, instance_str)
        instanced_aug_dir = os.path.join(BirdVox_wav_dir, instanced_aug_str)

        # Loop over recording units.
        for unit in units:
            unit_str = "unit" + str(unit).zfill(2)
            in_unit_dir = os.path.join(instanced_aug_dir, unit_str)

            gps_row = gps_df.loc[gps_df["Unit"] == "unit01"].iloc[0]
            latitude = gps_row["Latitude"]
            longitude = gps_row["Longitude"]
