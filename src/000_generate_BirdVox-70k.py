import datetime
import numpy as np
import os
import pandas as pd
import soundfile as sf
import sys
import time

import paths


# Define constants
data_dir = paths.get_data_dir()
orig_sr = 24000 # the sample rate of the full night data is 24 kHz
suffix_str = "original.wav"
args = sys.argv[1:]
unit_id = int(args[0])
units = [1, 2, 3, 5, 7, 10]
unit = units[unit_id]
n_units = len(units)

# Print header
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start")
print("Generating BirdVox-70k clips for unit " + str(unit).zfill(2))
print("")

# Create directory for original (i.e. non-augmented) clips
predictions_dir = os.path.join(data_dir, "random_forest_predictions")
recordings_dir = os.path.join(data_dir, "full_night_recordings")
annotations_dir = os.path.join(data_dir, "annotations")
clips_dir = os.path.join("data", "BirdVox-70k")
if not os.path.exists(clips_dir):
    os.makedirs(clips_dir)
original_clips_dir = os.path.join(clips_dir, "original")
if not os.path.exists(original_clips_dir):
    os.makedirs(original_clips_dir)

# Create directory corresponding to the recording unit
unit_str = "unit" + str(unit).zfill(2)
unit_dir = os.path.join(original_clips_dir, unit_str)
if not os.path.exists(unit_dir):
    os.makedirs(unit_dir)

# Open full night recording
samples = []
df = pd.read_csv(annotation_path, sep='\t')
recording_name = unit_str + ".flac"
recording_path = os.path.join(recordings_dir, recording_name)
full_night = sf.SoundFile(recording_path)
n_positive_samples = 0
n_negative_samples = 0

# Export every annotation either as positive (flight call) or negative (alarm)
for index, row in df.iterrows():
    # Compute center time of the annotation bounding box
    time = 0.5 * (row["Begin Time (s)"] + row["End Time (s)"])
    sample = int(24000 * time)
    sample_str = str(sample).zfill(9)
    # Compute center frequency of the annotation bounding box
    freq = 0.5 * (row["Low Freq (Hz)"] + row["High Freq (Hz)"])
    freq_str = str(int(freq)).zfill(4)
    comment = row["Calls"]
    # Alarm sounds are negative examples (label 0)
    if comment == "alarm":
        label_str = "0"
        n_negative_samples = n_negative_samples + 1
    # All other annotations are genuine flight calls (label 1)
    else:
        label_str = "1"
        n_positive_samples = n_positive_samples + 1
    clip_list = [unit_str, sample_str, freq_str, label_str, suffix_str]
    clip_str = "_".join(clip_list)
    # The start of the clip is 250 ms before the annotation
    sample_start = sample - 6000
    full_night.seek(sample_start)
    # The end of the clip is 250 ms after the annotation
    data = full_night.read(12000)
    clip_path = os.path.join(original_clips_dir)
    sf.write(clip_str, data, orig_sr)
    samples.append(sample)

# The number of false positives to be added to the dataset is equal to the
# difference between the number of annotated positives (flight calls) and
# the number of annotated negatives (alarms)
n_false_positives = n_positive_samples - n_negative_samples
print("Number of positives (genuine flight calls): " + str(n_positive_samples))
print("Number of negatives (alarms): " + str(n_negative_samples))
print("Number of false positives (clips fooling SKM-based detector): "
      + str(n_false_positives))
print("Total number of clips: " + str(2*n_positive_samples))
print("")

# Load probabilities of the SKM (spherical k-means) prediction model
# developed by Justin Salamon
prediction_name = unit_str + "_skm_prob.npy"
prediction_path = os.path.join(predictions_dir, prediction_name)
prob_matrix = np.load(prediction_path)

# Retrieve timestamps corresponding to decreasing confidences
prob_samples = (prob_matrix[:, 0] * 24000).astype('int')
probs = prob_matrix[:, 1]
sorting_indices = np.argsort(probs)[::-1]
sorted_probs = probs[sorting_indices]
sorted_prob_samples = prob_samples[sorting_indices]
sorted_prob_samples = sorted_prob_samples

# The exported false positives correspond to the timestamps with highest
# confidences under the condition that they are 6000 samples (500 ms) apart
# from all previously exported clips
prob_counter = 0
false_positive_counter = 0
while false_positive_counter < n_false_positives:
    prob_sample = sorted_prob_samples[prob_counter]
    dists = [np.abs(sample-prob_sample) for sample in samples]
    if np.all([dist > 6000 for dist in dists]):
        samples.append(prob_sample)
        sample_str = str(prob_sample).zfill(9)
        # By convention, the frequency of a false positive example is 0 Hz
        freq_str = str(0).zfill(4)
        clip_list = [unit_str, sample_str, freq_str, "0", suffix_str]
        false_positive_counter = false_positive_counter + 1
        clip_str = "_".join(clip_list)
        sample_start = prob_sample - 6000
        full_night.seek(sample_start)
        data = full_night.read(12000)
        sf.write(clip_str, data, orig_sr)
    prob_counter = prob_counter + 1

# Print elapsed time
print(str(datetime.datetime.now()) + " Finish")
elapsed_time = time.time() - start_time
elapsed_hours = int(elapsed_time / (60 * 60))
elapsed_minutes = int((elapsed_time % (60 * 60)) / 60)
elapsed_seconds = elapsed_time % 60.
elapsed_str = "{:>02}:{:>02}:{:>05.2f}".format(elapsed_hours,
                                               elapsed_minutes,
                                               elapsed_seconds)
print("Total elapsed time: " + elapsed_str)
