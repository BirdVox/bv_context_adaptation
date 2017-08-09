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
data_dir = localodule.get_data_dir()
tolerances = localmodule.get_tolerances()


# Read command-line arguments.                           ENABLE
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


# Define directory for predictions.
oldbird_models_dir = os.path.join(models_dir, "oldbird")
unit_dir = os.path.join(oldbird_models_dir, unit_str)
predictions_name = "_".join(["predictions", clip_suppressor_str])
predictions_dir = os.path.join(unit_dir, predictions_name)


# Open annotation as Pandas DataFrame.
annotations_name = "_".join([dataset_name, "annotations"])
annotations_dir = os.path.join(data_dir, annotations_name)
annotation_name = unit_str + ".txt"
annotation_path = os.path.join(annotations_dir, annotation_name)
annotation_df = pd.read_csv(annotation_path, delimiter="\t")
begin_times = np.array(annotation_df["Begin Time (s)"]])
end_times = np.array(annotation_df["End Time (s)"])
true_times = 0.5 * (begin_times+end_times)

# Loop over tolerances.
tolerance = tolerances[0] #                             DISABLE
#for tolerance in tolerances:                           ENABLE



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
