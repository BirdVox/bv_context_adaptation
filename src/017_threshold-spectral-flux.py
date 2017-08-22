import csv
import datetime
import h5py
import numpy as np
import os
import sys
import time

import localmodule


# Define constants.
n_thresholds = 100
data_dir = localmodule.get_data_dir()
dataset_name = localmodule.get_dataset_name()
models_dir = localmodule.get_models_dir()
args = sys.argv[1:]
unit_str = args[0]


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Thresholding spectral flux on " + dataset_name + ", " + unit_str + ".")
print('h5py version: {:s}.'.format(h5py.__version__))
print('numpy version: {:s}'.format(np.__version__))
print("")


# Load onset detection function.
sf_name = "_".join([dataset_name, "spectral-flux"])
sf_dir = os.path.join(data_dir, oldbird_name)
odf_path = os.path.join(oldbird_dir, unit_str + ".hdf5")
odf_file = h5py.File(odf_path, "r")
odf_dataset_key = "spectral-flux_odf"
odf = odf_file[odf_dataset_key]
odf_length = odf.shape[1]


# Create CSV header.
csv_header = [
    'Dataset',
    'Unit',
    'ODF',
    'Threshold ID',
    'Threshold',
    'Time (s)',
    'Onset ODF']


# Close HDF5 file.
odf_file.close()


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
