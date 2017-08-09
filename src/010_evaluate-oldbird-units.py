import datetime
import numpy as np
import os
import pandas as pd
import sys
import time

import localmodule


# Define constants.
dataset_name = localmodule.get_datset_name()
models_dir = localmodule.get_models_dir()
oldbird_models_dir = os.path.join(models_dir, "oldbird")
#args = sys.argv[1:]
#unit_str = args[0]
#odf_str = args[1]
#suppressor_str = args[2]
unit_str = "unit01"
odf_str = "thrush"
clip_suppressor_str = "clip-suppressor"


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Evaluating Old Bird on " + dataset_name + ", " + unit_str + ".")
print('numpy version: {:s}'.format(np.__version__))
print('pandas version: {:s}'.format(pd.__version__))
print("")


# Loop over tolerances.


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
