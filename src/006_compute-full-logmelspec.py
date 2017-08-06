import datetime
import h5py
import librosa
import os
import pandas as pd
import sys
import time

sys.path.append('../src') #                                    DISABLE
import localmodule



# Define constants.
data_dir = localmodule.get_data_dir()
dataset_name = localmodule.get_dataset_name()
# args = sys.argv[1:]                                           ENABLE
args = ["unit01"] #                                             DISABLE
unit_str = args[0]
logmelspec_settings = localmodule.get_logmelspec_settings()


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Computing log-mel-spectrograms (logmelspec) for full " + dataset_name + ".")
print("Unit: " + unit_str + ".")
print("")
print("h5py version: {:s}".format(h5py.__version__))
print("librosa version: {:s}".format(librosa.__version__))
print("pandas version: {:s}".format(pd.__version__))
print("")


# Create HDF5 container of logmelspecs
full_logmelspec_name = "_".join([dataset_name, "full_logmelspec"])
full_logmelspec_dir = os.path.join(data_dir, full_logmelspec_name)
os.makedirs(full_logmelspec_dir, exist_ok=True)
out_name = unit_str
out_path = os.path.join(full_logmelspec_dir, out_name + ".hdf5")
out_file = h5py.File(out_path)


# Load GPS coordinates.
gps_name = "_".join([dataset_name, "gps-coordinates.csv"])
gps_path = os.path.join(data_dir, gps_name)
gps_df = pd.read_csv(gps_path)
gps_row = gps_df.loc[gps_df["Unit"] == unit_str].iloc[0]


# Load UTC starting times.
utc_name = "_".join([dataset_name, "utc-start-times.csv"])
utc_path = os.path.join(data_dir, utc_name)
utc_df = pd.read_csv(utc_path)
utc_row = utc_df.loc[utc_df["Unit"] == unit_str].iloc[0]


# Copy over metadata.
out_file["dataset_name"] = localmodule.get_dataset_name()
out_file["unit"] = unit_str
out_file["utc_start_time"] = utc_row["UTC"]
gps_group = out_file.create_group("gps_coordinates")
gps_group["latitude"] =  gps_row["Latitude"]
gps_group["longitude"] = gps_row["Longitude"]
settings_group = out_file.create_group("logmelspec_settings")
settings_group["fmax"] = logmelspec_settings["fmax"]
settings_group["fmin"] = logmelspec_settings["fmin"]
settings_group["hop_length"] = logmelspec_settings["hop_length"]
settings_group["n_fft"] = logmelspec_settings["n_fft"]
settings_group["n_mels"] = logmelspec_settings["n_mels"]
settings_group["sr"] = logmelspec_settings["sr"]
settings_group["win_length"] = logmelspec_settings["win_length"]
settings_group["window"] = logmelspec_settings["window"]


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
