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
chunk_duration = 60.0 # in seconds
chunk_length = int(np.round(chunk_duration * sample_rate))
chunk_padding_duration = 0.5 # in seconds
chunk_padding_length = int(np.round(chunk_padding_duration * sample_rate))


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
