import datetime
import numpy as np
import os
import pandas as pd
import soundfile as sf
import sys
import time

import paths


# Define constants.
data_dir = localmodule.get_data_dir()
dataset_name = localmodule.get_dataset_name()
dataset_wav_name = "_".join(dataset_name, "audio")
dataset_wav_dir = os.path.join(data_dir, dataset_wav_name)
original_dataset_wav_dir = os.path.join(dataset_wav_dir, "original")
units = localmodule.get_units()
clip_duration = 0.5


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Generating " + dataset_name + " JAMS metadata.")
print('jams version: {:s}'.format(jams.__version__) + ".")
print('muda version: {:s}'.format(muda.__version__) + ".")
print('numpy version: {:s}'.format(np.__version__) + ".")
print('librosa version: {:s}'.format(librosa.__version__) + ".")
print("")


# Loop over recording units.
for unit_str in units:
    unit_str = units[unit_id]
    unit_dir = os.path.join(original_BirdVox_wav_dir, unit_str)
    names = os.listdir(unit_dir)
    names = sorted(names)
    n_names = len(names)

    # Loop over names.
    for name_id in range(n_names):
        name = names[name_id]

        # Initialize JAMS metadata file.
        jam = jams.JAMS()

        # Create annotation.
        ann = jams.Annotation('tag_open')
        ann.duration = clip_duration

        # Add tag with snippet sound class.
        ann.append(time=0, duration=clip_duration, value=name[23], confidence=1)

        # Fill file metadata.
        jam.file_metadata.title = name[7:16]
        jam.file_metadata.release = '1.0'
        jam.file_metadata.duration = clip_duration
        jam.file_metadata.artist = name[:6]

        # Fill annotation metadata.
        ann.annotation_metadata.version = '1.0'
        ann.annotation_metadata.corpus = dataset_name

        # Add annotation.
        jam.annotations.append(ann)

        # Export JAM file.
        jam_name = name[:-3] + "jams"
        out_path = os.path.join(unit_dir, jam_name)
        jam.save(out_path)


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
