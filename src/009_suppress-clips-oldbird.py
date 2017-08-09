import datetime
import numpy as np
import os
import pandas as pd
import sys
import time

import localmodule


# Define constants.
args = ["unit01"] #                                     DISABLE
#args = sys.argv[1:]                                     ENABLE
unit_str = args[0]
dataset_name = localmodule.get_dataset_name()
data_dir = localmodule.get_data_dir()




# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Running Old Bird clip suppressor on " + dataset_name + ", " + unit_str + ".")
print('pandas version: {:s}'.format(pd.__version__))
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
