import datetime
import h5py
import itertools
import math
import numpy as np
import os
import pandas as pd
import soundfile as sf
import scipy
import sys
import time
import vesper.old_bird.old_bird_detector_redux as ob

import localmodule


def design_oldbird_filter(settings):
    f0 = settings.filter_f0
    f1 = settings.filter_f1
    bw = settings.filter_bw
    fs2 = localmodule.get_sample_rate()
    bands = np.array([0, f0 - bw, f0, f1, f1 + bw, fs2]) / fs2
    desired = np.array([0, 0, 1, 1, 0, 0])
    coefficients = ob._firls(settings.filter_length, bands, desired)
    return coefficients


# Define constants.
data_dir = localmodule.get_data_dir()
dataset_name = localmodule.get_dataset_name()
full_audio_name = "_".join([dataset_name, "full-audio"])
full_audio_dir = os.path.join(data_dir, full_audio_name)
sample_rate = localmodule.get_sample_rate()
args = sys.argv[1:]
unit_str = args[0]
chunk_duration = 60.0 # in seconds
chunk_length = int(np.round(chunk_duration * sample_rate))
chunk_padding_duration = 0.5 # in seconds
chunk_padding_length = int(np.round(chunk_padding_duration * sample_rate))


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Running Old Bird onset detection functions (Thrush and Tseep) on " +
    dataset_name + ", " + unit_str + ".")
print('h5py version: {:s}.'.format(h5py.__version__))
print('numpy version: {:s}'.format(np.__version__))
print('pandas version: {:s}'.format(pd.__version__))
print('scipy version: {:s}'.format(scipy.__version__))
print('soundfile version: {:s}'.format(sf.__version__))
print("")


# Create HDF5 container of ODF curves
full_oldbird_name = "_".join([dataset_name, "oldbird"])
full_oldbird_dir = os.path.join(data_dir, full_oldbird_name)
os.makedirs(full_oldbird_dir, exist_ok=True)
out_name = unit_str
out_path = os.path.join(full_oldbird_dir, out_name + ".hdf5")
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


# Design Thrush filter and integrator.
thrush_settings = ob._THRUSH_SETTINGS
thrush_fir = design_oldbird_filter(thrush_settings)
thrush_integration_time = thrush_settings.integration_time
thrush_integration_length = int(round(thrush_integration_time * sample_rate))
thrush_integrator = np.ones(thrush_integration_length)
thrush_integrator = thrush_integrator / thrush_integration_length
thrush_delay = math.floor(thrush_settings.ratio_delay * sample_rate)
thrush_group = out_file.create_group("thrush_settings")
for thrush_key in thrush_settings.__dict__:
    thrush_group[thrush_key] = thrush_settings.__dict__[thrush_key]


# Design Tseep filter and integrator.
tseep_settings = ob._TSEEP_SETTINGS
tseep_fir = design_oldbird_filter(tseep_settings)
tseep_integration_time = tseep_settings.integration_time
tseep_integration_length = int(round(tseep_integration_time * sample_rate))
tseep_integrator = np.ones(tseep_integration_length)
tseep_integrator = tseep_integrator / tseep_integration_length
tseep_delay = math.floor(tseep_settings.ratio_delay * sample_rate)
tseep_group = out_file.create_group("tseep_settings")
for tseep_key in tseep_settings.__dict__:
    tseep_group[tseep_key] = tseep_settings.__dict__[tseep_key]


# Count number of chunks.
in_unit_path = os.path.join(full_audio_dir, unit_str + ".flac")
full_audio_object = sf.SoundFile(in_unit_path)
full_audio_length = len(full_audio_object)
n_chunks = int(np.ceil(full_audio_length / chunk_length))


# Initialize datasets of onset detection functions (ODF).
dataset_size = (1, full_audio_length)
thrush_dataset = out_file.create_dataset("thrush_odf", dataset_size)
tseep_dataset = out_file.create_dataset("tseep_odf", dataset_size)


# Loop over chunks.
for chunk_id in range(n_chunks):
    # Load audio excerpt.
    chunk_start = chunk_id * chunk_length
    chunk_stop = min(chunk_start + chunk_length, full_audio_length)

    # Read prefix padding.
    pre_padding_start = max(chunk_start-chunk_padding_length, 0)
    full_audio_object.seek(pre_padding_start)
    pre_padding = full_audio_object.read(chunk_padding_length)

    # Read chunk.
    full_audio_object.seek(chunk_start)
    chunk = full_audio_object.read(chunk_stop-chunk_start)

    # Read suffix padding.
    post_padding_start = min(chunk_stop, full_audio_length-chunk_padding_length)
    full_audio_object.seek(post_padding_start)
    post_padding = full_audio_object.read(chunk_padding_length)

    # Concatenate prefix, chunk, and suffix.
    padded_chunk = np.concatenate((pre_padding, chunk, post_padding))

    # Apply Thrush filter, square, integrate, divide by delayed signal, unpad.
    fir_thrush = scipy.signal.fftconvolve(padded_chunk, thrush_fir, mode="same")
    squared_thrush = fir_thrush * fir_thrush
    integrated_thrush = scipy.signal.fftconvolve(squared_thrush,
        thrush_integrator, mode="same")
    thrush_padding = np.empty(thrush_delay)
    thrush_padding.fill(integrated_thrush[-1])
    thrush_tuple = (integrated_thrush[thrush_delay:], thrush_padding)
    delayed_thrush = np.concatenate(thrush_tuple)
    thrush_odf = delayed_thrush / integrated_thrush
    thrush_chunk_odf = thrush_odf[chunk_padding_length:-chunk_padding_length]
    thrush_chunk_odf = thrush_chunk_odf.astype('float32')
    thrush_dataset[0, chunk_start:chunk_stop] = thrush_chunk_odf

    # Apply Tseep filter, square, integrate, divide by delayed signal.
    fir_tseep = scipy.signal.fftconvolve(padded_chunk, tseep_fir, mode="same")
    squared_tseep = fir_tseep * fir_tseep
    integrated_tseep = scipy.signal.fftconvolve(squared_tseep,
        tseep_integrator, mode="same")
    tseep_padding = np.empty(tseep_delay)
    tseep_padding.fill(integrated_tseep[-1])
    tseep_tuple = (integrated_tseep[tseep_delay:], tseep_padding)
    delayed_tseep = np.concatenate(tseep_tuple)
    tseep_odf = delayed_tseep / integrated_tseep
    tseep_chunk_odf = tseep_odf[chunk_padding_length:-chunk_padding_length]
    tseep_chunk_odf = tseep_chunk_odf.astype('float32')
    tseep_dataset[0, chunk_start:chunk_stop] = tseep_chunk_odf


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
