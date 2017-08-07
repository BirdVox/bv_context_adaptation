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
logmelspec_settings = localmodule.get_logmelspec_settings()
sample_rate = localmodule.get_sample_rate()
chunk_duration = logmelspec_settings["hop_length"] # in seconds
chunk_length = chunk_duration * sample_rate


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Computing log-mel-spectrograms (logmelspec) for full " +
    dataset_name + ".")
print("Unit: " + unit_str + ".")
print("")
print("h5py version: {:s}".format(h5py.__version__))
print("librosa version: {:s}".format(librosa.__version__))
print("numpy version: {:s}".format(np.__version__))
print("pandas version: {:s}".format(pd.__version__))
print("soundfile version: {:s}".format(sf.__version__))
print("")


# Create HDF5 container of logmelspecs
full_logmelspec_name = "_".join([dataset_name, "full-logmelspec"])
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
out_file["dataset_name"] = dataset_name
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


# Open full audio file as FLAC.
recordings_name = "_".join([dataset_name, "full-audio"])
recordings_dir = os.path.join(data_dir, recordings_name)
recording_name = unit_str + ".flac"
recording_path = os.path.join(recordings_dir, recording_name)
full_audio = sf.SoundFile(recording_path)
full_audio_length = len(full_audio)


# Define a time sample for the middle of every audio clip.
lms_sr = logmelspec_settings["sr"]
lms_hop_length = logmelspec_settings["hop_length"]
sample_float_step = lms_hop_length * sample_rate / lms_sr
n_hops = int(np.floor(full_audio_length / sample_float_step))
n_chunks = int(np.ceil(n_clips / n_clips_per_chunk))
samples_per_hop = lms_hop_length * sample_rate / lms_sr


# Start HDF5 group for log-mel-spectrograms (logmelspec).
lms_dataset_size = (logmelspec_settings["n_mels"], n_hops)
lms_dataset = out_file.create_dataset("logmelspec", lms_dataset_size)

# Loop over chunks.
for chunk_id in [0, n_chunks-1]: # debug mode
#for chunk_id in range(n_chunks):
    # Load audio chunk.
    first_hop = chunk_id * n_hops_per_chunk
    chunk_start = int(np.ceil(first_hop * sample_float_step))
    last_hop = min((chunk_id+1) * n_hops_per_chunk, n_hops)
    chunk_stop = int(np.floor(last_hop * sample_float_step))
    full_audio.seek(chunk_start)
    chunk_waveform = full_audio.read(chunk_stop-chunk_start)

    # Resample to 22050 Hz.
    chunk_waveform = librosa.resample(
        chunk_waveform, sample_rate, logmelspec_settings["sr"])

    # Compute Short-Term Fourier Transform (STFT).
    stft = librosa.stft(
        chunk_waveform,
        n_fft=logmelspec_settings["n_fft"],
        win_length=logmelspec_settings["win_length"],
        hop_length=logmelspec_settings["hop_length"],
        window=logmelspec_settings["window"])

    # Delete last sample to compensante for padding.
    stft = stft[:, :-1]

    # Compute squared magnitude coefficients.
    abs2_stft = (stft.real*stft.real) + (stft.imag*stft.imag)

    # Gather frequency bins according to the Mel scale.
    melspec = librosa.feature.melspectrogram(
        y=None,
        S=abs2_stft,
        sr=logmelspec_settings["sr"],
        n_fft=logmelspec_settings["n_fft"],
        n_mels=logmelspec_settings["n_mels"],
        htk=True,
        fmin=logmelspec_settings["fmin"],
        fmax=logmelspec_settings["fmax"])

    # Apply pointwise base-10 logarithm.
    # The multiplication by 0.5 is to compensate for magnitude squaring.
    logmelspec = 0.5 * librosa.logamplitude(melspec, ref=1.0)

    # Convert to single floating-point precision.
    logmelspec = logmelspec.astype('float32')

    # Write to HDF5 dataset.
    # hop_start is an integer because chunk_start is both a multiple
    # of sample_rate and lms_hop_length = chunk_duration.
    hop_start = int((chunk_start*lms_sr) / (sample_rate*lms_hop_length))
    n_hops_in_chunk = logmelspec.shape[1]
    hop_stop = hop_start + n_hops_in_chunk
    lms_dataset[:, hop_start:hop_stop] = logmelspec


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
