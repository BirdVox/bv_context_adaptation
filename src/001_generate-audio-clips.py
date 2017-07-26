import datetime
import numpy as np
import os
import pandas as pd
import soundfile as sf
import sys
import time

import localmodule


# Define constants.
data_dir = localmodule.get_data_dir()
dataset_name = localmodule.get_dataset_name()
orig_sr = localmodule.get_sample_rate()
negative_labels = localmodule.get_negative_labels()
clip_length = int(0.500 * orig_sr) # a clip lasts 500 ms
args = sys.argv[1:]
unit_str = args[0]
units = localmodule.get_units()
n_units = len(units)


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Generating " + dataset_name + " clips for " + unit_str + ".")
print('numpy version: {:s}.'.format(np.__version__))
print('pandas version: {:s}.'.format(pd.__version__))
print('soundfile version: {:s}.'.format(sf.__version__))
print("")


# Create directory for original (i.e. non-augmented) clips.
predictions_name = "_".join([dataset_name, "baseline-predictions"])
predictions_dir = os.path.join(data_dir, predictions_name)
recordings_name = "_".join([dataset_name, "full-audio"])
recordings_dir = os.path.join(data_dir, recordings_name)
annotations_name = "_".join([dataset_name, "annotations"])
annotations_dir = os.path.join(data_dir, annotations_dir)
dataset_wav_name = "_".join([dataset_name, "audio-clips"])
dataset_wav_dir = os.path.join(data_dir, dataset_wav_name)
if not os.path.exists(dataset_wav_dir):
    os.makedirs(dataset_wav_dir)
original_dataset_wav_dir = os.path.join(dataset_wav_dir, "original")
if not os.path.exists(original_dataset_wav_dir):
    os.makedirs(original_dataset_wav_dir)


# Create directory corresponding to the recording unit.
unit_dir = os.path.join(original_dataset_wav_dir, unit_str)
if not os.path.exists(unit_dir):
    os.makedirs(unit_dir)


# Open full night recording.
samples = []
annotation_name = unit_str + ".txt"
annotation_path = os.path.join(annotations_dir, annotation_name)
df = pd.read_csv(annotation_path, sep='\t')
recording_name = unit_str + ".flac"
recording_path = os.path.join(recordings_dir, recording_name)
full_night = sf.SoundFile(recording_path)
n_positive_samples = 0
n_negative_samples = 0


# Export every annotation either as positive (flight call) or negative (alarm).
for index, row in df.iterrows():
    # Compute center time of the annotation bounding box.
    mid_time = 0.5 * (row["Begin Time (s)"] + row["End Time (s)"])
    sample = int(orig_sr * mid_time)
    sample_str = str(sample).zfill(9)

    # Compute center frequency of the annotation bounding box.
    mid_freq = 0.5 * (row["Low Freq (Hz)"] + row["High Freq (Hz)"])
    freq_str = str(int(mid_freq)).zfill(5)
    if "Calls" in row and row["Calls"] in negative_labels:
        label_str = "0"
        n_negative_samples = n_negative_samples + 1
    else:
        label_str = "1"
        n_positive_samples = n_positive_samples + 1
    clip_list = [unit_str, sample_str, freq_str, label_str, suffix_str]
    clip_str = "_".join(clip_list)

    # Read.
    sample_start = sample - int(0.5 * clip_length)
    full_night.seek(sample_start)
    data = full_night.read(clip_length)

    # Export.
    clip_path = os.path.join(unit_dir, clip_str)
    sf.write(clip_path, data, orig_sr)
    samples.append(sample)


# The number of false positives to be added to the dataset is equal to the
# difference between the number of annotated positives and
# the number of annotated negatives.
n_false_positives = n_positive_samples - n_negative_samples
print("Number of positives: " + str(n_positive_samples) + ".")
print("Number of negatives: " + str(n_negative_samples) + ".")
print("Number of false positives (clips fooling baseline detector): "
      + str(n_false_positives) + ".")
print("Total number of clips: " + str(2*n_positive_samples) + ".")
print("")


# Load probabilities of the baseline prediction model.
prediction_name = unit_str + ".npy"
prediction_path = os.path.join(predictions_dir, prediction_name)
prob_matrix = np.load(prediction_path)


# Retrieve timestamps corresponding to decreasing confidences.
prob_samples = (prob_matrix[:, 0] * orig_sr).astype('int')
probs = prob_matrix[:, 1]
sorting_indices = np.argsort(probs)[::-1]
sorted_probs = probs[sorting_indices]
sorted_prob_samples = prob_samples[sorting_indices]
sorted_prob_samples = sorted_prob_samples


# The exported false positives correspond to the timestamps with highest
# confidences under the condition that they are 6000 samples (500 ms) apart
# from all previously exported clips.
prob_counter = 0
false_positive_counter = 0
while false_positive_counter < n_false_positives:
    prob_sample = sorted_prob_samples[prob_counter]
    dists = [np.abs(sample-prob_sample) for sample in samples]
    min_dist = np.min(dists)
    if min_dist > clip_length:
        # Append sample to growing list.
        samples.append(prob_sample)
        sample_str = str(prob_sample).zfill(9)

        # By convention, the frequency of a false positive example is 0 Hz.
        freq_str = str(0).zfill(5)
        clip_list = [unit_str, sample_str, freq_str, "0", "original.wav"]
        false_positive_counter = false_positive_counter + 1
        clip_str = "_".join(clip_list)

        # Read.
        sample_start = prob_sample - int(0.5 * clip_length)
        full_night.seek(sample_start)
        data = full_night.read(clip_length)

        # Export.
        clip_path = os.path.join(unit_dir, clip_str)
        sf.write(clip_path, data, orig_sr)
    prob_counter = prob_counter + 1


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
