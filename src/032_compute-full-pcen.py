import datetime
import h5py
import librosa
import numpy as np
import os
import pandas as pd
import soundfile as sf
import sys
import time

import localmodule


# Define constants.
data_dir = localmodule.get_data_dir()
dataset_name = localmodule.get_dataset_name()
args = sys.argv[1:]
unit_str = args[0]
pcen_settings = localmodule.get_pcen_settings()
sample_rate = localmodule.get_sample_rate()
chunk_duration = pcen_settings["hop_length"] # in seconds
chunk_length = chunk_duration * sample_rate


# Define PCEN smoother.
def pcen_smooth(melspec, time_constant_frames):
    smoothed_melspec = melspec.copy()
    coeff = 1.0 / time_constant_frames
    num_cols = melspec.shape[1]
    for col in np.arange(1, num_cols):
        smoothed_melspec[:, col] =\
            smoothed_melspec[:, col - 1] +\
            (melspec[:, col] - smoothed_melspec[:, col - 1]) * coeff
    return smoothed_melspec


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Computing PCEN for full " + dataset_name + ".")
print("Unit: " + unit_str + ".")
print("")
print("h5py version: {:s}".format(h5py.__version__))
print("librosa version: {:s}".format(librosa.__version__))
print("numpy version: {:s}".format(np.__version__))
print("pandas version: {:s}".format(pd.__version__))
print("soundfile version: {:s}".format(sf.__version__))
print("")


# Create HDF5 container of PCENs
full_pcen_name = "_".join([dataset_name, "full-pcen"])
full_pcen_dir = os.path.join(data_dir, full_pcen_name)
os.makedirs(full_pcen_dir, exist_ok=True)
out_name = unit_str
out_path = os.path.join(full_pcen_dir, out_name + ".hdf5")
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
out_file["utc_start_time"] = utc_row["UTC"]
gps_group = out_file.create_group("gps_coordinates")
gps_group["latitude"] =  gps_row["Latitude"]
gps_group["longitude"] = gps_row["Longitude"]
settings_group = out_file.create_group("pcen_settings")
settings_group["fmax"] = pcen_settings["fmax"]
settings_group["fmin"] = pcen_settings["fmin"]
settings_group["hop_length"] = pcen_settings["hop_length"]
settings_group["n_fft"] = pcen_settings["n_fft"]
settings_group["n_mels"] = pcen_settings["n_mels"]
settings_group["sr"] = pcen_settings["sr"]
settings_group["win_length"] = pcen_settings["win_length"]
settings_group["window"] = pcen_settings["window"]
settings_group["pcen_delta_denominator"] =\
    pcen_settings["pcen_delta_denominator"]
settings_group["pcen_time_constant_frames"] =\
    pcen_settings["pcen_time_constant_frames"]
settings_group["pcen_norm_exponent"] =\
    pcen_settings["pcen_norm_exponent"]
settings_group["pcen_power"] =\
    pcen_settings["pcen_power"]


# Open full audio file as FLAC.
recordings_name = "_".join([dataset_name, "full-audio"])
recordings_dir = os.path.join(data_dir, recordings_name)
recording_name = unit_str + ".flac"
recording_path = os.path.join(recordings_dir, recording_name)
full_audio = sf.SoundFile(recording_path)
full_audio_length = len(full_audio)


# Compute number of chunks and number of hops.
n_chunks = int(np.ceil(full_audio_length / chunk_length))
pcen_hop_length = pcen_settings["hop_length"]
pcen_sr = pcen_settings["sr"]
n_samples_per_hop = pcen_hop_length * sample_rate / pcen_sr
n_hops = int(np.floor(full_audio_length / n_samples_per_hop))


# Start HDF5 group for per-channel energy normalization (PCEN) spectrograms.
pcen_dataset_size = (pcen_settings["n_mels"], n_hops)
pcen_dataset = out_file.create_dataset("pcen", pcen_dataset_size)


# Loop over chunks.
for chunk_id in range(n_chunks):

    # Load audio chunk.
    chunk_start = chunk_id * chunk_length
    chunk_stop = min(chunk_start + chunk_length, full_audio_length)
    full_audio.seek(chunk_start)
    chunk_waveform = full_audio.read(chunk_stop-chunk_start)
    chunk_waveform = chunk_waveform * (2**32)

    # Resample to 22050 Hz.
    chunk_waveform = librosa.resample(
        chunk_waveform, sample_rate, pcen_settings["sr"])

    # Compute Short-Term Fourier Transform (STFT).
    stft = librosa.stft(
        chunk_waveform,
        n_fft=pcen_settings["n_fft"],
        win_length=pcen_settings["win_length"],
        hop_length=pcen_settings["hop_length"],
        window=pcen_settings["window"])

    # Delete last sample to compensate for padding.
    stft = stft[:, :-1]

    # Compute squared magnitude coefficients.
    abs2_stft = (stft.real*stft.real) + (stft.imag*stft.imag)

    # Gather frequency bins according to the Mel scale.
    melspec = librosa.feature.melspectrogram(
        y=None,
        S=abs2_stft,
        sr=pcen_settings["sr"],
        n_fft=pcen_settings["n_fft"],
        n_mels=pcen_settings["n_mels"],
        htk=True,
        fmin=pcen_settings["fmin"],
        fmax=pcen_settings["fmax"])

    # Smooth mel-spectrogram.
    smoothed_melspec =\
        pcen_smooth(melspec, pcen_settings["pcen_time_constant_frames"])

    # Apply adaptive gain factor.
    pcen_gain = (smoothed_melspec + 1) ** pcen_settings["pcen_norm_exponent"]
    pcen_melspec = melspec * pcen_gain

    # Raise to PCEN exponent.
    pcen_offset = pcen_melspec.max() / 10.0
    pcen =\
        (pcen_melspec + pcen_offset) ** pcen_settings["pcen_power"] -\
        pcen_offset ** pcen_settings["pcen_power"]

    # Convert to single floating-point precision.
    pcen = pcen.astype('float32')

    # Write to HDF5 dataset.
    # hop_start is an integer because chunk_start is both a multiple
    # of sample_rate and pcen_hop_length = chunk_duration.
    hop_start = int((chunk_start*pcen_sr) / (sample_rate*pcen_hop_length))
    n_hops_in_chunk = pcen.shape[1]
    hop_stop = min(hop_start + n_hops_in_chunk, n_hops)
    pcen_dataset[:, hop_start:hop_stop] = pcen


# Close file.
out_file.close()


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
