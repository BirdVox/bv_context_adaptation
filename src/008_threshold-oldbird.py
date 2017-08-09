import csv
import datetime
import h5py
import numpy as np
import os
import sys
import time

import localmodule


# Define constants.
n_thresholds = 100
# The array of upward thresholds is equal to
# f(x) = t_0 + threshold_multiplier * (x**threshold_exponent)
# when the parameters threshold_multiplier and threshold_exponent
# are chosen such that:
# (1)    f(0.0)   = t_0
# (2)    f(alpha) = t_alpha
# (3)    f(1.0)   = t_1
# We arbitrarily set
# (a)    t_0     = 1.0
# (b)    t_alpha = ad_hoc_threshold
# (c)    t_1     = 2*ad_hoc_threshold - 1
# (d)    alpha = 0.5
# In Old Bird, ad_hoc_threshold is equal to 2.0 for Thrush and 1.2 for Tseep.
alpha = 0.5
data_dir = localmodule.get_data_dir()
dataset_name = localmodule.get_dataset_name()
models_dir = localmodule.get_models_dir()
sample_rate = localmodule.get_sample_rate()
hop_duration = 0.02 # in seconds
hop_length = int(np.round(sample_rate * hop_duration))
args = sys.argv[1:]
unit_str = args[0]
odf_str = args[1]
threshold_id_start = int(args[2][3:5])
threshold_id_stop = int(args[2][-2:])
threshold_id_range = range(threshold_id_start, 1 + threshold_id_stop)


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Running Old Bird onset detection functions (Thrush and Tseep) on " +
    dataset_name + ", " + unit_str + ".")
print('h5py version: {:s}.'.format(h5py.__version__))
print('numpy version: {:s}'.format(np.__version__))
print("")


# Load onset detection function.
oldbird_name = "_".join([dataset_name, "oldbird"])
oldbird_dir = os.path.join(data_dir, oldbird_name)
odf_path = os.path.join(oldbird_dir, unit_str + ".hdf5")
odf_file = h5py.File(odf_path, "r")
odf_dataset_key = "_".join([odf_str, "odf"])
odf = odf_file[odf_dataset_key]
odf_length = odf.shape[1]


# Define arrays of thresholds.
odf_settings_key = "_".join([odf_str, "settings"])
odf_settings = odf_file[odf_settings_key]
ad_hoc_threshold = odf_settings["ratio_threshold"].value
t_0 = 1.0
t_alpha = ad_hoc_threshold
t_1 = 2*ad_hoc_threshold - 1
threshold_multiplier = t_1 - t_0
threshold_exponent = (np.log(t_alpha-t_0) - np.log(t_1-t_0)) / np.log(alpha)
threshold_x = np.linspace(0, 1, 1+n_thresholds)[1:]
up_thresholds = t_0 + threshold_multiplier * (threshold_x**threshold_exponent)
down_thresholds = 1.0 / up_thresholds


# Create directory for Old Bird in models_dir.
model_dir = os.path.join(models_dir, "oldbird")
os.makedirs(model_dir, exist_ok=True)
out_unit_dir = os.path.join(model_dir, unit_str)
os.makedirs(out_unit_dir, exist_ok=True)
predictions_name = "_".join(["predictions", "no-clip-suppressor"])
predictions_dir = os.path.join(out_unit_dir, predictions_name)
os.makedirs(predictions_dir, exist_ok=True)


# Compute minimum and maximum clip length according to Old Bird heuristics.
min_clip_duration = odf_settings["min_duration"].value
min_clip_length = int(np.round(min_clip_duration * sample_rate))
max_clip_duration = odf_settings["max_duration"].value
max_clip_length = int(np.round(max_clip_duration * sample_rate))


# Create CSV header.
csv_header = [
    'Dataset',
    'Unit',
    'ODF',
    'Threshold ID',
    'Upward threshold',
    'Downward threshold',
    'Time (s)',
    'Duration (s)',
    'Onset ODF',
    'Offset ODF']


# Loop over thresholds.
for threshold_id in threshold_id_range:
    # Read upward threshold and downward threshold.
    up_threshold = up_thresholds[threshold_id]
    down_threshold = down_thresholds[threshold_id]
    threshold_str = str(threshold_id).zfill(2)

    # Create CSV file for predictions.
    csv_file_name = "_".join([dataset_name, "oldbird", odf_str, unit_str,
        "th-" + threshold_str, "predictions.csv"])
    csv_file_path = os.path.join(predictions_dir, csv_file_name)
    csv_file = open(csv_file_path, 'w')
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(csv_header)

    # Initialize variables.
    clip_start = 0
    clip_stop = 0
    clip_mid = 0
    onset_odf = 0.0
    offset_odf = 0.0
    clip_switch = False
    t = 0

    # Scan the whole onset detection function through time
    while t < odf_length:

        # If we are not inside a clip ...
        if (not clip_switch):

            # ... wait for an onset (odf[0, t] > up_threshold).
            if (odf[0, t] > up_threshold):
                # We are at the clip onset. Store start time and value of ODF.
                clip_switch = True
                clip_start = t
                onset_odf = odf[0, t]

        # Otherwise, if we are inside a clip, wait for an offset
        # (odf[t] < down_threshold) or until the maximum clip length is reached.
        elif (odf[0, t] < down_threshold) or ((t-clip_start) == max_clip_length):

            # We are at the clip offset.
            # If odf[t] > up_threshold, we should keep the clip_switch to True,
            # but that is not what Old Bird and Vesper do.
            # see https://github.com/HaroldMills/Vesper-Tseep-Thrush/blob/master/tests/test_old_bird_detector_redux.py#L63-L65
            clip_switch = False
            # Bound the clip length from below.
            clip_length = max(t-clip_start, min_clip_length)
            # Compute time at the middle of the clip and clip duration.
            clip_stop = min(clip_start + clip_length, odf_length - 1)
            clip_mid = int(0.5 * (clip_start+clip_stop))
            clip_time = clip_mid / sample_rate
            clip_duration = clip_length / sample_rate
            # Also store value of ODF at offset.
            offset_odf = odf[0, clip_stop]
            # Export clip_time, clip_duration, onset_odf, offset_odf.
            csv_header = [
                'Dataset',
                'Unit',
                'ODF',
                'Threshold ID',
                'Upward threshold',
                'Downward threshold',
                'Time (s)',
                'Duration (s)',
                'Onset ODF',
                'Offset ODF']
            row = [
                dataset_name,
                unit_str,
                'Old Bird (' + odf_str + ')',
                threshold_str,
                "{:5.3f}".format(up_threshold),
                "{:5.3f}".format(down_threshold),
                "{:8.2f}".format(clip_time),
                "{:5.3f}".format(clip_duration),
                "{:9.3f}".format(onset_odf),
                "{:5.3f}".format(offset_odf)]
            csv_writer.writerow(row)
            # If clip length is shorter than minimum, jump to the end of clip.
            if (t-clip_start) < min_clip_length:
                t = int(np.floor(clip_stop/hop_length)) * hop_length
        t = t + hop_length

    # If the ODF ends with an onset not followed by any offset, export clip
    # by using last timestamp as offset. This is unlikely to happen in practice.
    if clip_switch:
        clip_switch = False
        clip_stop = odf_length - 1
        clip_mid = int(0.5 * (clip_start+clip_stop))
        clip_time = clip_mid / sample_rate
        clip_duration = clip_length / sample_rate
        offset_odf = odf[0, clip_stop]
        row = [clip_time, clip_duration, onset_odf, offset_odf]
        csv_writer.writerow(row)


# Close CSV file.
csv_file.close()


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
