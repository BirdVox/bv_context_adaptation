import os

import localmodule


# Define constants.
data_dir = localmodule.get_data_dir()
dataset_name = localmodule.get_dataset_name()
dataset_wav_name = "_".join([dataset_name, "audio-clips"])
dataset_wav_dir = os.path.join(data_dir, dataset_wav_name)
archive_dir = localmodule.get_archive_dir()


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Archiving " + dataset_name + " audio clips with JAMS metadata.")
print("h5py version: {:s}".format(h5py.__version__))
print("pandas version: {:s}".format(pd.__version__))
print("")


#
