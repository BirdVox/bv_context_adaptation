import datetime
import h5py
import librosa
import os
import sys
import time

import localmodule


# Define constants.
data_dir = localmodule.get_data_dir()
dataset_name = localmodule.get_dataset_name()
sample_rate = localmodule.get_sample_rate()
args = ["stretch", 0, "unit01"] #                          DISABLE ME
#args = sys.argv[1:]                                         ENABLE ME
aug_str = args[0]
instance_id = int(args[1])
instance_str = str(instance_id)
unit_str = args[2]
if aug_str == "original":
    instanced_aug_str = aug_str
else:
    instanced_aug_str = "-".join([aug_str, instance_str])
logmelspec_settings = localmodule.get_logmelspec_settings()


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Computing log-mel-spectrograms (logmelspec) for " + dataset_name + ".")
print("Unit: " + unit_str + ".")
print("Augmentation: " + instanced_aug_str + ".")
print("")
print("h5py version: {:s}".format(h5py.__version__))
print("librosa version: {:s}".format(librosa.__version__))
print("")


# Open HDF5 container of waveforms
hdf5_dataset_name = "_".join([dataset_name, "hdf5"])
hdf5_dir = os.path.join(data_dir, hdf5_dataset_name)
in_aug_dir = os.path.join(hdf5_dir, aug_str)
hdf5_name = "_".join([dataset_name, instanced_aug_str, unit_str])
in_path = os.path.join(in_aug_dir, hdf5_name + ".hdf5")
in_file = h5py.File(in_path, "r")


# Create HDF5 container of logmelspecs
logmelspec_name = "_".join([dataset_name, "logmelspec"])
logmelspec_dir = os.path.join(data_dir, logmelspec_name)
os.makedirs(logmelspec_dir, exist_ok=True)
out_aug_dir = os.path.join(logmelspec_dir, aug_str)
os.makedirs(out_aug_dir, exist_ok=True)
out_path = os.path.join(out_aug_dir, hdf5_name + ".hdf5")
out_file = h5py.File(out_path)

# Copy over metadata
#out_file["gps_coordinates"] = in_file["gps_coordinates"]
out_file["dataset_name"] = localmodule.get_dataset_name()
out_file["unit"] = unit_str
out_file["augmentation"] = aug_str
out_file["instance"] = instance_id
out_file["settings"] = logmelspec_settings
out_file["utc_start_time"] = in_file["utc_start_time"].value
#waveforms = in_file["waveforms"]
#durations = [waveforms[key].shape[0] for key in waveforms.keys()]


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
