import datetime
import glob
import jams
import h5py
import librosa
import os
import pandas as pd
import soundfile as sf
import time

import localmodule


# Define constants.
data_dir = localmodule.get_data_dir()
dataset_name = localmodule.get_dataset_name()
dataset_wav_name = "_".join([dataset_name, "audio-clips"])
dataset_wav_dir = os.path.join(data_dir, dataset_wav_name)
units = localmodule.get_units()
augmentations = localmodule.get_augmentations()
sample_rate = localmodule.get_sample_rate()


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Saving " + dataset_name + " audio data and metadata into HDF5 containers.")
print("h5py version: {:s}".format(h5py.__version__))
print("jams version: {:s}".format(jams.__version__))
print("librosa version: {:s}".format(librosa.__version__))
print("pandas version: {:s}".format(pd.__version__))
print("soundfile version: {:s}".format(sf.__version__))
print("")


# Create directory for HDF5 data.
dataset_hdf5_name = "_".join([dataset_name, "hdf5"])
dataset_hdf5_dir = os.path.join(data_dir, dataset_hdf5_name)
if not os.path.exists(dataset_hdf5_dir):
    os.makedirs(dataset_hdf5_dir)


# Load GPS coordinates as Pandas dataframe.
gps_name = "_".join([dataset_name, "gps-coordinates.csv"])
gps_path = os.path.join(data_dir, gps_name)
gps_df = pd.read_csv(gps_path)


# Load UTC starting times.
utc_name = "_".join([dataset_name, "utc-start-times.csv"])
utc_path = os.path.join(data_dir, utc_name)
utc_df = pd.read_csv(utc_path)


# Loop over augmentations.
for aug_str in augmentations:
    n_instances = augmentations[aug_str]

    aug_dir = os.path.join(dataset_hdf5_dir, aug_str)
    if not os.path.exists(aug_dir):
        os.makedirs(aug_dir)

    # Loop over instances.
    for instance_id in range(n_instances):
        # Define directory for instanced augmentation.
        if aug_str == "original":
            in_instanced_aug_str = aug_str
            out_instanced_aug_str = aug_str
        else:
            instance_str = str(instance_id)
            in_instanced_aug_str = "_".join([aug_str, instance_str])
            out_instanced_aug_str = "-".join([aug_str, instance_str])
        in_instanced_aug_dir = os.path.join(
            dataset_wav_dir, in_instanced_aug_str)
        out_instanced_aug_dir = os.path.join(
            dataset_wav_dir, out_instanced_aug_str)

        # Loop over recording units.
        for unit_str in units:
            # Initialize HDF5 container.
            file_name = "_".join(
                [dataset_name, out_instanced_aug_str, unit_str])
            file_path = os.path.join(aug_dir, file_name + ".hdf5")
            f = h5py.File(file_path, "w")

            # Write latitude and longitude.
            gps_row = gps_df.loc[gps_df["Unit"] == unit_str].iloc[0]
            gps_group = f.create_group("gps_coordinates")
            gps_group["latitude"] = gps_row["Latitude"]
            gps_group["longitude"] = gps_row["Longitude"]

            # Write starting time.
            utc_row = utc_df.loc[utc_df["Unit"] == unit_str].iloc[0]
            f["utc_start_time"] = utc_row["UTC"]

            # List clips in unit.
            in_unit_dir = os.path.join(in_instanced_aug_dir, unit_str)
            wav_paths = glob.glob(os.path.join(in_unit_dir, "*.wav"))
            wav_paths = sorted(wav_paths)

            # Loop over clips.
            waveform_group = f.create_group("waveforms")
            for wav_path in wav_paths:
                waveform = librosa.load(wav_path, sr=sample_rate)[0]
                clip_name = os.path.split(wav_path)[1][:-4]
                waveform_group[clip_name] = waveform

            # Write sample rate
            f["sample_rate"] = sample_rate


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
