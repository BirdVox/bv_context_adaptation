import datetime
import h5py
import numpy as np
import os
import sys
import time

sys.path.append("../src")
import localmodule


# Define constants.
dataset_name = localmodule.get_dataset_name()
full_logmelspec_name = "_".join([
    dataset_name, "full-logmelspec"])
data_dir = localmodule.get_data_dir()
full_logmelspec_dir = os.path.join(
    data_dir, full_logmelspec_name)
orig_sr = localmodule.get_sample_rate()
percentiles = [0.1, 1, 10, 25, 50, 75, 90, 99, 99.9]
n_percentiles = len(percentiles)


# Parse input arguments.
args = sys.argv[1:]
T_str = args[0]
unit_str = args[1]
bg_duration = int(T_str)


# Create folder for backgrounds.
backgrounds_name = "_".join(
    [dataset_name, "full-backgrounds"])
backgrounds_dir = os.path.join(data_dir, backgrounds_name)
os.makedirs(backgrounds_dir, exist_ok=True)


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Computing background summaries on " + dataset_name + " full nights.")
print("Background duration (T): " + T_str + ".")
print("Unit: " + unit_str + ".")
print("")
print("h5py version: {:s}".format(h5py.__version__))
print("numpy version: {:s}".format(np.__version__))
print("")


# Open full night data.
in_full_unit_name = unit_str + ".hdf5"
in_full_unit_path = os.path.join(
    full_logmelspec_dir, in_full_unit_name)
in_full_unit_file = h5py.File(in_full_unit_path, "r")
in_full_group = in_full_unit_file["logmelspec"]
n_bins, n_hops = in_full_group.shape


# Load settings.
lms_hop_length = 32
lms_sr = 24000
lms_ratio = lms_hop_length / lms_sr * orig_sr
lms_hop_duration = lms_hop_length / lms_sr


# Define duration of background in LMS hops.
bg_width = int(np.round(bg_duration * lms_sr / lms_hop_length))
bg_hop = int(np.round(0.25 * bg_width))
n_bg_hops = int(n_hops / bg_hop)


# Open file of full night data.
bg_duration_str = str(int(bg_duration)).zfill(4)
out_T_name = "-".join(["T", str(bg_duration_str)])
out_T_dir = os.path.join(backgrounds_dir, out_T_name)
os.makedirs(out_T_dir, exist_ok=True)
out_unit_name = "_".join([
    dataset_name, "full-backgrounds",
    unit_str, out_T_name]) + ".hdf5"
out_unit_path = os.path.join(out_T_dir, out_unit_name)
out_unit_file = h5py.File(out_unit_path, "w")
out_lms_group = out_unit_file.create_dataset(
    "logmelspec_background", (n_percentiles, n_bins, n_bg_hops))


# Load over clips.
for bg_hop_id in range(n_bg_hops):

    # Load background excerpt.
    lms_start = bg_hop_id * bg_hop
    lms_stop = min(lms_start + bg_width, n_hops)
    lms = in_full_group[:, lms_start:lms_stop]

    # Compute summary statistics.
    lms_percentiles = np.percentile(lms, percentiles, axis=1)

    # Store summary statistics.
    out_lms_group[:, :, bg_hop_id] = lms_percentiles

    if (bg_hop_id % 100) == 0:
        elapsed_time = time.time() - int(start_time)
        elapsed_hours = int(elapsed_time / (60 * 60))
        elapsed_minutes = int((elapsed_time % (60 * 60)) / 60)
        elapsed_seconds = elapsed_time % 60.
        elapsed_str = "{:>02}:{:>02}:{:>05.2f}".format(elapsed_hours,
                                                       elapsed_minutes,
                                                       elapsed_seconds)
        print("Total elapsed time: " + elapsed_str + ".")
        start_time = int(time.time())


# Close files.
in_full_unit_file.close()
out_unit_file.close()


# Print footer.
print(str(datetime.datetime.now()) + " Finish.")
elapsed_time = time.time() - int(start_time)
elapsed_hours = int(elapsed_time / (60 * 60))
elapsed_minutes = int((elapsed_time % (60 * 60)) / 60)
elapsed_seconds = elapsed_time % 60.
elapsed_str = "{:>02}:{:>02}:{:>05.2f}".format(elapsed_hours,
                                               elapsed_minutes,
                                               elapsed_seconds)
print("Total elapsed time: " + elapsed_str + ".")
