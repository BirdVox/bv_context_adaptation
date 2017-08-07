import datetime
import h5py
import numpy as np
import os
import time

import localmodule


# Define constants
dataset_name = localdmodule.get_dataset_name()
models_dir = localmodule.get_models_dir()
args = ["unit01", "thrush", "00:09"] #                          DISABLE
#args = sys.argv[1:]                                            ENABLE
unit_str = args[0]
odf_str = args[1]
threshold_id_start = int(args[2][:2])
threshold_id_stop = int(args[2][-2:])
threshold_id_range = range(threshold_id_start, threshold_id_stop)


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Running Old Bird onset detection functions (Thrush and Tseep) on " +
    dataset_name + ", " + unit_str + ".")
print('h5py version: {:s}.'.format(h5py.__version__))
print('numpy version: {:s}'.format(np.__version__))
print("")


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
