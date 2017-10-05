import datetime
import time
import os
import sys

import localmodule


# Define constants.
args = sys.argv[1:]
aug_str = args[0]
instance_id = int(args[1])
instance_str = str(instance_id)
unit_str = args[2]
if aug_str == "original":
    instanced_aug_str = aug_str
else:
    instanced_aug_str = "-".join([aug_str, instance_str])


# Define HDF5 path.
data_dir = localmodule.get_data_dir()
dataset_name = localmodule.get_dataset_name()
hdf5_dir = "_".join([dataset_name, "hdf5"])
hdf5_dir_path = os.path.join(data_dir, hdf5_dir)
augmentation_dir_path = os.path.join(hdf5_dir_path, instanced_aug_str)
hdf5_name = "_".join([dataset_name, instanced_aug_str, unit_str])
hdf5_path = os.path.join(augmentation_dir_path, hdf5_name + ".hdf5")


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Computing scattering coefficients for " + dataset_name + ".")
print("Unit: " + unit_str + ".")
print("Augmentation: " + instanced_aug_str + ".")
print("")


# Define scattering path.
scattering_path = os.path.expanduser(os.path.join("~", "scattering.m"))
src_path = os.path.join("..", "..", "..", "src")


# Define MATLAB code.
matlab_code = "; ".join([
    "addpath(genpath('" + scattering_path + "'))",
    "addpath('" + src_path + "')",
    "hdf5_path = '" + hdf5_path + "'",
    "compute_scattering_snowball(hdf5_path)",
    "quit;"])


# Define UNIX command.
unix_command = "matlab -r \"" + matlab_code + "\""


# Call UNIX command.
os.system(unix_command)


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
