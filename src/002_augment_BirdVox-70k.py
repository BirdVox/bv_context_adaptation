import datetime
import numpy as np
import os
import pandas as pd
import soundfile as sf
import sys
import time

import localmodule


# Define constants
data_dir = localmodule.get_data_dir()
args = sys.argv[1:]
aug_str = args[0]
unit_id = int(args[1])
units = localmodule.get_units()
unit = units[unit_id]
n_units = len(units)

# Print header
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start")
print("Augmenting BirdVox-70k clips for unit " + str(unit).zfill(2))
print("")

# Create directory for augmented clips
clips_dir = os.path.join(data_dir, "BirdVox-70k")
if not os.path.exists(clips_dir):
    os.makedirs(clips_dir)
aug_clips_dir = os.path.join(clips_dir, aug_str)
if not os.path.exists(aug_clips_dir):
    os.makedirs(aug_clips_dir)

# Create directory corresponding to the recording unit
unit_str = "unit" + str(unit).zfill(2)
unit_dir = os.path.join(aug_clips_dir, unit_str)
if not os.path.exists(unit_dir):
    os.makedirs(unit_dir)



# Print elapsed time
print(str(datetime.datetime.now()) + " Finish")
elapsed_time = time.time() - int(start_time)
elapsed_hours = int(elapsed_time / (60 * 60))
elapsed_minutes = int((elapsed_time % (60 * 60)) / 60)
elapsed_seconds = elapsed_time % 60.
elapsed_str = "{:>02}:{:>02}:{:>05.2f}".format(elapsed_hours,
                                               elapsed_minutes,
                                               elapsed_seconds)
print("Total elapsed time: " + elapsed_str)
