import datetime
import h5py
import itertools
import librosa
import math
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
full_audio_name = "_".join([dataset_name, "full-audio"])
full_audio_dir = os.path.join(data_dir, full_audio_name)
sample_rate = localmodule.get_sample_rate()
args = sys.argv[1:]
unit_str = args[0]
chunk_duration = 64 # in seconds
chunk_length = chunk_duration * sample_rate


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Running spectral flux on " + dataset_name + ", " + unit_str + ".")
print('h5py version: {:s}.'.format(h5py.__version__))
print('librosa version: {:s}.'.format(librosa.__version__))
print('numpy version: {:s}'.format(np.__version__))
print('pandas version: {:s}'.format(pd.__version__))
print('soundfile version: {:s}'.format(sf.__version__))
print("")


# Create HDF5 container of ODF curves.
full_spectralflux_name = "_".join([dataset_name, "spectral-flux"])
full_spectralflux_dir = os.path.join(data_dir, full_spectralflux_name)
os.makedirs(full_spectralflux_dir, exist_ok=True)
out_name = unit_str
out_path = os.path.join(full_spectralflux_dir, out_name + ".hdf5")
out_file = h5py.File(out_path)


# Load GPS coordinates.
gps_name = "_".join([dataset_name, "gps-coordinates.csv"])
gps_path = os.path.join(data_dir, gps_name)
gps_df = pd.read_csv(gps_path)
gps_row = gps_df.loc[gps_df["Unit"] == unit_str].iloc[0]


# Load UTC starting times.
utc_name = "_".join([dataset_name, "utc-start-times.csv"])
utc_path = os.path.join(data_dir, utc_name)
utc_df = pd.read_csv(utc_path)
utc_row = utc_df.loc[utc_df["Unit"] == unit_str].iloc[0]


# Copy over metadata.
out_file["dataset_name"] = dataset_name
out_file["unit"] = unit_str
out_file["sample_rate"] = sample_rate
out_file["utc_start_time"] = utc_row["UTC"]
gps_group = out_file.create_group("gps_coordinates")
gps_group["latitude"] =  gps_row["Latitude"]
gps_group["longitude"] = gps_row["Longitude"]


# Open full audio file as FLAC.
recordings_name = "_".join([dataset_name, "full-audio"])
recordings_dir = os.path.join(data_dir, recordings_name)
recording_name = unit_str + ".flac"
recording_path = os.path.join(recordings_dir, recording_name)
full_audio = sf.SoundFile(recording_path)
full_audio_length = len(full_audio)


# Initialize dataset of onset detection function (ODF).
dataset_size = (1, full_audio_length)
spectralflux_dataset = out_file.create_dataset(
    "spectral-flux_odf", dataset_size)


# Loop over chunks.
for chunk_id in range(n_chunks):
    # Load audio chunk.
    chunk_start = chunk_id * chunk_length
    chunk_stop = min(chunk_start + chunk_length, full_audio_length)
    full_audio.seek(chunk_start)
    chunk_waveform = full_audio.read(chunk_stop-chunk_start)

    # Compute spectral flux.
    odf = librosa.onset.onset_strength(chunk_waveform)

    # Delete last sample to compensate for padding.
    odf = odf[:-1]
