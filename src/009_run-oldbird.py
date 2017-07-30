import itertools
import math
import numpy as np
import os
import soundfile as sf
import scipy
import sys
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
chunk_duration = 600.0 # in seconds
chunk_length = chunk_duration * sample_rate
chunk_padding_duration = 5.0 # in seconds
chunk_padding_length = chunk_padding_duration * sample_rate


# Design Thrush filter and integrator
thrush_settings = os._THRUSH_SETTINGS
thrush_fir = design_oldbird_filter(thrush_settings)
thrush_integration_time = thrush_settings.integration_time
thrush_integration_length = int(round(thrush_integration_time * sample_rate))
thrush_integrator = np.ones(thrush_integration_length)
thrush_integrator = thrush_integrator / thrush_integration_length
thrush_delay = math.floor(thrush_settings.ratio_delay * sample_rate)
thrush_threshold = thrush_settings.threshold
thrush_inv_threshold = 1. / thrush_threshold


# Design Tseep filter and integrator
tseep_settings = ob._TSEEP_SETTINGS
tseep_fir = design_oldbird_filter(tseep_settings)
tseep_integration_time = tseep_settings.integration_time
tseep_integration_length = int(round(tseep_integration_time * sample_rate))
tseep_integrator = np.ones(tseep_integrator)
tseep_integrator = tseep_integrator / tseep_integration_length
tseep_delay = math.floor(tseep_settings.ratio_delay * sample_rate)
tseep_threshold = tseep_settings.threshold
tseep_inv_threshold = 1. / tseep_threshold


# Count number of chunks
in_unit_path = os.path.join(full_audio_dir, unit_str + ".flac")
full_audio_object = sf.SoundFile(in_unit_path)
full_audio_length = len(full_audio_object)
n_chunks = int(np.ceil(full_audio_length / chunk_length))


# Initialize lists of onset detection functions (ODF)
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

    # Apply Thrush filter, square, integrate, divide by delayed signal, unpad
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

    # Apply Tseep filter, square, integrate, divide by delayed signal
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


# Concatenate chunk-wise ODFs to get full ODFs for the whole unit
thrush_odf = np.concatenate(thrush_chunk_odfs)
tseep_odf = np.concatenate(tseep_chunk_odfs)
