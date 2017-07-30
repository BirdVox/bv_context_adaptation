import datetime
import itertools
import math
import numpy as np
import os
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
chunk_length = chunk_duration * sample_rate
chunk_padding_duration = 0.5 # in seconds
chunk_padding_length = chunk_padding_duration * sample_rate


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Generating " + dataset_name + " clips for " + unit_str + ".")
print('numpy version: {:s}'.format(np.__version__))
print('scipy version: {:s}'.format(scipy.__version__))
print('soundfile version: {:s}'.format(sf.__version__))
print("")


# Design Thrush filter and integrator.
thrush_settings = os._THRUSH_SETTINGS
thrush_fir = design_oldbird_filter(thrush_settings)
thrush_integration_time = thrush_settings.integration_time
thrush_integration_length = int(round(thrush_integration_time * sample_rate))
thrush_integrator = np.ones(thrush_integration_length)
thrush_integrator = thrush_integrator / thrush_integration_length
thrush_delay = math.floor(thrush_settings.ratio_delay * sample_rate)


# Design Tseep filter and integrator.
tseep_settings = ob._TSEEP_SETTINGS
tseep_fir = design_oldbird_filter(tseep_settings)
tseep_integration_time = tseep_settings.integration_time
tseep_integration_length = int(round(tseep_integration_time * sample_rate))
tseep_integrator = np.ones(tseep_integrator)
tseep_integrator = tseep_integrator / tseep_integration_length
tseep_delay = math.floor(tseep_settings.ratio_delay * sample_rate)


# Count number of chunks.
in_unit_path = os.path.join(full_audio_dir, unit_str + ".flac")
full_audio_object = sf.SoundFile(in_unit_path)
full_audio_length = len(full_audio_object)
n_chunks = int(np.ceil(full_audio_length / chunk_length))


# Initialize lists of onset detection functions (ODF).
thrush_chunk_odfs = []
tseep_chunk_odfs = []


# Loop over chunks.
for chunk_id in range(n_chunks):
    # Load audio excerpt.
    chunk_id = 0
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
    full_audio_object.seek(pos_padding_start)
    post_padding = full_audio_object.read(chunk_padding_length)

    # Concatenate prefix, chunk, and suffix.
    padded_chunk = np.concatenate((pre_padding, chunk, post_padding))

    # Apply Thrush filter, square, integrate, divide by delayed signal, unpad.
    fir_thrush = scipy.signal.fftconvolve(padded_chunk, thrush_fir, mode='valid')
    squared_thrush = fir_thrush * fir_thrush
    integrated_thrush = scipy.signal.fftconvolve(squared_thrush, thrush_integrator)
    thrush_padding = np.empty(thrush_delay)
    thrush_padding.fill(integrated_tseep[0])
    thrush_tuple = (thrush_padding, integrated_thrush)
    delayed_thrush = np.concatenate(thrush_tuple)
    thrush_odf = delayed_thrush / integrated_thrush
    thrush_chunk_odf = thrush_odf[chunk_padding_length:-chunk_padding_length]
    thrush_chunk_odfs.append(thrush_chunk_odf)

    # Apply Tseep filter, square, integrate, divide by delayed signal.
    fir_tseep = scipy.signal.fftconvolve(signal, tseep_fir, mode='valid')
    squared_tseep = fir_tseep * fir_tseep
    integrated_tseep = scipy.signal.fftconvolve(squared_tseep, tseep_integrator)
    tseep_padding = np.empty(tseep_delay)
    tseep_padding.fill(integrated_tseep[0])
    tseep_tuple = (tseep_padding, integrated_tseep)
    delayed_tseep = np.concatenate(tseep_tuple)
    tseep_odf = delayed_tseep / integrated_tseep
    tseep_chunk_odf = tseep_odf[chunk_padding_length:-chunk_padding_length]
    tseep_chunk_odfs.append(tseep_chunk_odf)


# Concatenate chunk-wise ODFs to get full ODFs for the whole unit.
thrush_odf = np.concatenate(thrush_chunk_odfs)
tseep_odf = np.concatenate(tseep_chunk_odfs)


# Renormalize Thrush and Tseep ODFs by their respective thresholds, and sum
# the results to get a global ODF.
thrush_threshold = thrush_settings.threshold
tseep_threshold = tseep_settings.threshold
global_odf = 0.5 * (thruh_odf/thrush_threshold + tseep_odf/tseep_threshold)


# Build numpy matrices. The first column is a timestamp, the second column is
# the unnormalized probability.
time = np.linspace(0, full_audio_length, endpoint=False)
thrush_matrix = np.stack((time, thrush_odf), axis=-1)
tseep_matrix = np.stack((time, tseep_odf), axis=-1)
global_matrix = np.stack((time, global_odf), axis=-1)


# Export matrices related to Thrush, Tseep, and "global".
models_dir = localmodule.get_data_dir()
model_name = os.path.basename(__file__).split("_")[0]
model_dir = os.path.join(models_dir, model_dir)
os.makedirs(model_dir, exist_ok=True)
out_unit_dir = os.path.join(model_dir, unit_str)
os.makedirs(out_unit_dir, exit_ok=True)
thrush_filename = "_".join([model_name, "thrush-odf", unit_str, "0"]) + ".npy"
thrush_path = os.path.join(out_unit_dir, thrush_filename)
np.save(thrush_path, thrush_matrix)
tseep_filename = "_".join([model_name, "tseep-odf", unit_str, "0"]) + ".npy"
tseep_path = os.path.join(out_unit_dir, tseep_filename)
np.save(tseep_path, tseep_matrix)
global_filename = "_".join([model_name, "odf", unit_str, "0"]) + ".npy"
global_path = os.path.join(out_unit_dir, global_filename)
np.save(global_path, global_matrix)


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
