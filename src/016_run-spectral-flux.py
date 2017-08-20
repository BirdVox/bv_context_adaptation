import datetime
import h5py
import librosa
import numpy as np
import os
import soundfile as sf
import sys
import time

import localmodule


# Define constants.
data_dir = localmodule.get_data_dir()
dataset_name = localmodule.get_dataset_name()
full_audio_name = "_".join([dataset_name, "full-audio"])
full_audio_dir = os.path.join(data_dir, full_audio_name)
sample_rate = localmodule.get_sample_rate()
args = sys.argv[1:]
unit_str = args[0]
sf_hop_length = 512 # default value for melspectrogram in librosa
sf_sr = 22050 # defaut value for sample rate in librosa
chunk_duration = 256 # in seconds
chunk_length = chunk_duration * sample_rate


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Running spectral flux on " + dataset_name + ", " + unit_str + ".")
print('h5py version: {:s}.'.format(h5py.__version__))
print('librosa version: {:s}.'.format(librosa.__version__))
print('numpy version: {:s}'.format(np.__version__))
print('soundfile version: {:s}'.format(sf.__version__))
print("")


# Create HDF5 container of ODF curves.
full_spectralflux_name = "_".join([dataset_name, "spectral-flux"])
full_spectralflux_dir = os.path.join(data_dir, full_spectralflux_name)
os.makedirs(full_spectralflux_dir, exist_ok=True)
out_name = unit_str
out_path = os.path.join(full_spectralflux_dir, out_name + ".hdf5")
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
out_file["dataset_name"] = dataset_name
out_file["unit"] = unit_str
out_file["sample_rate"] = sample_rate
out_file["utc_start_time"] = utc_row["UTC"]
gps_group = out_file.create_group("gps_coordinates")
gps_group["latitude"] =  gps_row["Latitude"]
gps_group["longitude"] = gps_row["Longitude"]


# Open full audio file as FLAC.
recordings_name = "_".join([dataset_name, "full-audio"])
recordings_dir = os.path.join(data_dir, recordings_name)
recording_name = unit_str + ".flac"
recording_path = os.path.join(recordings_dir, recording_name)
full_audio = sf.SoundFile(recording_path)
full_audio_length = len(full_audio)


# Compute number of chunks and number of hops.
n_chunks = int(np.ceil(full_audio_length / chunk_length))
n_samples_per_hop = sf_hop_length * sample_rate / sf_sr
n_hops = int(np.floor(full_audio_length / n_samples_per_hop))


# Initialize dataset of onset detection function (ODF).
dataset_size = (1, n_hops)
spectralflux_dataset = out_file.create_dataset(
    "spectral-flux_odf", dataset_size)


# Loop over chunks.
for chunk_id in range(n_chunks):
    # Load audio chunk.
    chunk_start = chunk_id * chunk_length
    chunk_stop = min(chunk_start + chunk_length, full_audio_length)
    full_audio.seek(chunk_start)
    chunk_waveform = full_audio.read(chunk_stop-chunk_start)

    # Compute spectral flux.
    odf = librosa.onset.onset_strength(chunk_waveform)

    # Delete last sample to compensate for padding.
    odf = odf[:-1]

    # Convert to single floating-point precision.
    odf = odf.astype('float32')

    # Write to HDF5 dataset.
    # hop_start is an integer because chunk_start is both a multiple
    # of sample_rate and hop_length = chunk_duration.
    hop_start = int((chunk_start*sf_sr) / (sample_rate*sf_hop_length))
    n_hops_in_chunk = odf.shape[0]
    hop_stop = min(hop_start + n_hops_in_chunk, n_hops)
    spectralflux_dataset[:, hop_start:hop_stop] = odf


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
