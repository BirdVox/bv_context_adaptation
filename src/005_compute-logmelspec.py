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
args = ["original", 0, "unit01"] #                          DISABLE ME
#args = sys.argv[1:]                                         ENABLE ME
aug_str = args[0]
instance_str = str(int(args[1]))
unit_str = args[2]
if aug_str == "original":
    instanced_aug_str = aug_str
else:
    instanced_aug_str = "-".join([aug_str, instance_str])


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


# Define folder for logmelspec
logmelspec_name = "_".join([dataset_name, "logmelspec"])
logmelspec_dir = os.path.join(data_dir, logmelspec_name)
os.makedirs(logmelspec_dir, exist_ok=True)
aug_dir = os.path.join(logmelspec_dir, aug_str)
os.makedirs(aug_dir, exist_ok=True)
out_unit_dir = os.path.join(aug_dir, unit_str)
os.makedirs(out_unit_dir, exist_ok=True)
in_unit_dir = os.path.join(data_dir, )



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
