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
threshold_id_start = int(args[1][3:5])
threshold_id_stop = int(args[1][-2:])
threshold_id_range = range(threshold_id_start, 1 + threshold_id_stop)


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Thresholding spectral flux on " + dataset_name + ", " + unit_str + ".")
print('h5py version: {:s}.'.format(h5py.__version__))
print('numpy version: {:s}'.format(np.__version__))
print("")


# Find global minimum and maximum.
unit_maxima = []
for aux_unit_str in units:
    aux_odf_path = os.path.join(sf_dir, aux_unit_str + ".hdf5")
    with h5py.File(aux_odf_path, "r") as aux_odf_file:
        aux_odf = aux_odf_file[odf_dataset_key]
        unit_maximum = np.max(aux_odf)
        unit_maxima.append(unit_maximum)
max_threshold = max(unit_maxima)
min_threshold = 0.5 * max_threshold


# Define array of thresholds.
thresholds = np.linspace(min_threshold, max_threshold, n_thresholds)


# Load onset detection function.
sf_name = "_".join([dataset_name, "spectral-flux"])
sf_dir = os.path.join(data_dir, sf_name)
odf_path = os.path.join(sf_dir, unit_str + ".hdf5")
odf_file = h5py.File(odf_path, "r")
odf_dataset_key = "spectral-flux_odf"
odf = odf_file[odf_dataset_key]
odf_length = odf.shape[1]


# Create directory for Old Bird in models_dir.
model_dir = os.path.join(models_dir, "spectral-flux")
os.makedirs(model_dir, exist_ok=True)
out_unit_dir = os.path.join(model_dir, unit_str)
os.makedirs(out_unit_dir, exist_ok=True)
predictions_name = "predictions"
predictions_dir = os.path.join(out_unit_dir, predictions_name)
os.makedirs(predictions_dir, exist_ok=True)


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
