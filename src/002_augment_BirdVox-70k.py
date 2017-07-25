import datetime
import jams
import librosa
import muda
import glob
import os
import sys
import time

import localmodule


# Define constants
data_dir = localmodule.get_data_dir()
units = localmodule.get_units()
args = sys.argv[1:]
unit = int(args[0])
aug_str = args[1]

# Print header
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start")
print("Augmenting BirdVox-70k clips for unit " + str(unit).zfill(2))
print("jams version: {:s}'.format(jams.__version__)")
print("librosa version: {:s}'.format(librosa.__version__)")
print("muda version: {:s}'.format(muda.__version__)")
print("numpy version: {:s}'.format(numpy.__version__)")
print("")

# Create directory for augmented clips
clips_dir = os.path.join(data_dir, "BirdVox-70k")
if not os.path.exists(clips_dir):
    os.makedirs(clips_dir)
original_clips_dir = os.path.join(clips_dir, "original")
aug_clips_dir = os.path.join(clips_dir, aug_str)
if not os.path.exists(aug_clips_dir):
    os.makedirs(aug_clips_dir)

# Create directory corresponding to the recording unit
unit_str = "unit" + str(unit).zfill(2)
in_unit_dir = os.path.join(original_clips_dir, unit_str)
out_unit_dir = os.path.join(aug_clips_dir, unit_str)
if not os.path.exists(out_unit_dir):
    os.makedirs(out_unit_dir)

# Define deformers
if aug_str == "noise":
    # Background noise deformers
    noise_deformers = []
    for unit in units:
        # For each recording unit, we create a deformer which adds a negative
        # example (i.e. containing no flight call) to the current clip, weighted
        # by a randomized amplitude factor ranging between 0.1 and 0.5.
        # This does not change the label because
        # negative + negative = negative
        # and
        # positive + negative = positive
        unit_str = str(unit).zfill(2)
        unit_dir = os.path.join(original_clips_dir, unit_str)
        # This regular expression selects only negative, non-augmented examples
        # for background noise
        regexp = "*_0_original.wav"
        names = sorted(glob.glob(os.path.join(unit_dir, regexp)))
        unit_noise_paths = [os.path.join(unit_dir, name) for name in names]
        unit_noise_deformer = muda.deformers.BackgroundNoise(
            n_samples=2, files=unit_noise_paths, weight_min=0.1, weight_max=0.5)
        noise_deformers.append(unit_noise_deformer)
elif aug_str == "pitch":
    # Pitch shift deformer
    # For every clip to be augmented, we apply 4 pitch shifts whose intervals
    # are sampled from a normal distribution with null mean and unit variance,
    # as measured in semitones according to the 12-tone equal temperament.
    pitch_deformer = muda.deformers.RandomPitchShift(
        n_samples=4, mean=0.0, sigma=1.0)
elif aug_str == "stretch":
    # Time stretching deformer
    # For every clip to be augmented, we apply 4 time stretching whose factors
    # are sampled from a log-normal distribution with mu=0.0 and sigma=1.0.
    stretch_deformer = muda.deformers.RandomTimeStretch(
        n_samples=4, location=0.0, scale=0.1)

deformers = noise_deformers + [pitch_deformer, stretch_deformer]
wav_names = sorted(glob.glob(os.path.join(in_unit_dir)))


# Print elapsed time
print(str(datetime.datetime.now()) + " Finish")
elapsed_time = time.time() - int(start_time)
elapsed_hours = int(elapsed_time / (60 * 60))
elapsed_minutes = int((elapsed_time % (60 * 60)) / 60)
elapsed_seconds = elapsed_time % 60.
elapsed_str = "{:>02}:{:>02}:{:>05.2f}".format(elapsed_hours,
                                               elapsed_minutes,
                                               elapsed_seconds)
print("Total elapsed time: " + elapsed_str)
