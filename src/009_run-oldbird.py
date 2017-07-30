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


# Design Thrush filter and integrator
thrush_settings = os._THRUSH_SETTINGS
thrush_fir = design_oldbird_filter(thrush_settings)
thrush_integration_time = thrush_settings.integration_time
thrush_integration_length = int(round(thrush_integration_time * sample_rate))
thrush_integrator = np.ones(thrush_integration_length)
thrush_integrator = thrush_integrator / thrush_integration_length
thrush_delay = math.floor(thrush_settings.ratio_delay * sample_rate)


# Design Tseep filter and integrator
tseep_settings = ob._TSEEP_SETTINGS
tseep_fir = design_oldbird_filter(tseep_settings)
tseep_integration_time = tseep_settings.integration_time
tseep_integration_length = int(round(tseep_integration_time * sample_rate))
tseep_integrator = np.ones(tseep_integrator)
tseep_integrator = tseep_integrator / tseep_integration_length
tseep_delay = math.floor(tseep_settings.ratio_delay * sample_rate)


# Load audio excerpt.
signal_start = 3600 * sample_rate
signal_length = 60 * sample_rate
in_unit_path = os.path.join(full_audio_dir, unit_str + ".flac")
full_audio_object = sf.SoundFile(in_unit_path)
full_audio_object.seek(signal_start)
signal = full_audio_object.read(signal_length)


# Apply Thrush filter, square, integrate, divide by delayed signal
fir_thrush = scipy.signal.fftconvolve(signal, thrush_fir, mode='valid')
squared_thrush = fir_thrush * fir_thrush
integrated_thrush = scipy.signal.fftconvolve(squared_thrush, thrush_integrator)
thrush_padding = np.empty(thrush_delay)
thrush_padding.fill(integrated_tseep[0])
thrush_tuple = (thrush_padding, nintegrated_thrush[thrush_delay:])
delayed_thrush = np.concatenate(thrush_tuple)
divided_thrush = delayed_thrush / integrated_thrush


# Apply Tseep filter, square, integrate, divide by delayed signal
fir_tseep = scipy.signal.fftconvolve(signal, tseep_fir, mode='valid')
squared_tseep = fir_tseep * fir_tseep
integrated_tseep = scipy.signal.fftconvolve(squared_tseep, tseep_integrator)
tseep_padding = np.empty(tseep_delay)
tseep_padding.fill(integrated_tseep[0])
tseep_tuple = (tseep_padding, nintegrated_tseep[tseep_delay:])
delayed_tseep = np.concatenate(tseep_tuple)
divided_tseep = delayed_tseep / integrated_tseep
