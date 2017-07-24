import datetime
import jams
import librosa
import muda
import glob
import os
import sys
import time

import localmodule


# Define constants
data_dir = localmodule.get_data_dir()
units = localmodule.get_units()
args = sys.argv[1:]
unit = int(args[0])
aug_str = args[1]
other_units = units.remove(unit)

# Print header
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start")
print("Augmenting BirdVox-70k clips for unit " + str(unit).zfill(2))
print("jams version: {:s}'.format(jams.__version__)")
print("librosa version: {:s}'.format(librosa.__version__)")
print("muda version: {:s}'.format(muda.__version__)")
print("numpy version: {:s}'.format(numpy.__version__)")
print("")

# Create directory for augmented clips
clips_dir = os.path.join(data_dir, "BirdVox-70k")
if not os.path.exists(clips_dir):
    os.makedirs(clips_dir)
original_clips_dir = os.path.join(clips_dir, "original")
aug_clips_dir = os.path.join(clips_dir, aug_str)
if not os.path.exists(aug_clips_dir):
    os.makedirs(aug_clips_dir)

# Create directory corresponding to the recording unit
unit_str = "unit" + str(unit).zfill(2)
in_unit_dir = os.path.join(original_clips_dir, unit_str)
out_unit_dir = os.path.join(aug_clips_dir, unit_str)
if not os.path.exists(out_unit_dir):
    os.makedirs(out_unit_dir)



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
