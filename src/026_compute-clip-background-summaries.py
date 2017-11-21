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
clip_logmelspec_name = "_".join([
    dataset_name, "logmelspec"])
clip_logmelspec_dir = os.path.join(
    data_dir, clip_logmelspec_name, "original")
orig_sr = localmodule.get_sample_rate()
percentiles = [0.1, 1, 10, 25, 50, 75, 90, 99, 99.9]


# Parse input arguments.
args = sys.argv[1:]
T_str = args[0]
unit_str = args[1]
bg_duration = int(T_str)


# Create folder for backgrounds.
backgrounds_name = "_".join(
    [dataset_name, "clip-backgrounds"])
backgrounds_dir = os.path.join(data_dir, backgrounds_name)
os.makedirs(backgrounds_dir, exist_ok=True)


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Computing background summaries on " + dataset_name + ".")
print("Background duration (T): " + T_str + ".")
print("Unit: " + unit_str + ".")
print("")
print("h5py version: {:s}".format(h5py.__version__))
print("numpy version: {:s}".format(np.__version__))
print("")


# Open file of clips.
in_full_unit_name = unit_str + ".hdf5"
in_full_unit_path = os.path.join(
    full_logmelspec_dir, in_full_unit_name)
in_full_unit_file = h5py.File(in_full_unit_path, "r")
in_full_group = in_full_unit_file["logmelspec"]
in_clip_unit_name = "_".join([
    dataset_name, "original", unit_str + ".hdf5"])
in_clip_unit_path = os.path.join(
    clip_logmelspec_dir, in_clip_unit_name)
in_clip_unit_file = h5py.File(in_clip_unit_path, "r")


# Load settings.
in_clip_group = in_clip_unit_file["logmelspec"]
in_clip_keys = list(in_clip_group.keys())
lms_settings = in_clip_unit_file["logmelspec_settings"]
lms_hop_length = lms_settings["hop_length"].value
lms_sr = lms_settings["sr"].value
lms_ratio = lms_hop_length / lms_sr * orig_sr
lms_hop_duration = lms_hop_length / lms_sr


# Define duration of background in LMS hops.
half_bg_duration = 0.5 * bg_duration
half_bg_width = int(np.round(
    half_bg_duration * lms_sr / lms_hop_length))


# Open file of full night data.
bg_duration_str = str(int(bg_duration)).zfill(4)
out_T_name = "-".join(["T", str(bg_duration_str)])
out_T_dir = os.path.join(backgrounds_dir, out_T_name)
os.makedirs(out_T_dir, exist_ok=True)
out_unit_name = "_".join([
    dataset_name, "clip-backgrounds",
    unit_str, out_T_name]) + ".hdf5"
out_unit_path = os.path.join(out_T_dir, out_unit_name)
out_unit_file = h5py.File(out_unit_path, "w")
out_lms_group =\
    out_unit_file.create_group("logmelspec_background")


# Load over clips.
is_end_reached = False
for in_clip_key in in_clip_keys:
    in_clip_key_list = in_clip_key.split("_")

    if not is_end_reached:

        # Load background excerpt.
        timestamp = int(in_clip_key_list[1])
        lms_mid = int(np.round(timestamp / lms_ratio))
        lms_start = max(0, lms_mid - half_bg_width)
        lms_stop = lms_start + 2 * half_bg_width


        if lms_stop > in_full_group.shape[1]:
            # Activate switch for end reached.
            #is_end_reached = True
            lms_stop = in_full_group.shape[1]

        lms_start = lms_stop - 2 * half_bg_width
        lms = in_full_group[:, lms_start:lms_stop]

        # Compute summary statistics.
        lms_percentiles = np.percentile(lms, percentiles, axis=1)

    # Store summary statistics.
    out_clip_key_list = in_clip_key_list[:-1]
    out_clip_key = "_".join(out_clip_key_list)
    out_lms_group[out_clip_key] = lms_percentiles


# Close files.
out_unit_file.close()
in_full_unit_file.close()
in_clip_unit_file.close()


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
