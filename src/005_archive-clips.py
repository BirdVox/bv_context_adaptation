import os


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Archiving " + dataset_name + " audio clips with JAMS metadata.")
print("h5py version: {:s}.".format(h5py.__version__))
print("pandas version: {:s}.".format(pd.__version__))
print("")
