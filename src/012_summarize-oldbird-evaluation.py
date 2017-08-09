import datetime
import numpy as np
import os
import pandas as pd
import time

import localmodule


# Define constants.
dataset_name = localmodule.get_dataset_name()

# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Summarizing Old Bird evaluation on " + dataset_name + ".")
print('numpy version: {:s}'.format(np.__version__))
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
