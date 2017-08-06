import datetime
import h5py
import librosa
import os
import pandas as pd
import soundfile as sf
import sys
import time

import localmodule


# Define constants.
data_dir = localmodule.get_data_dir()
dataset_name = localmodule.get_dataset_name()
# args = sys.argv[1:]                                           ENABLE
args = ["unit01"] #                                             DISABLE
unit_str = args[0]
logmelspec_settings = localmodule.get_logmelspec_settings()
n_clips_per_chunk = 1000


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Computing log-mel-spectrograms (logmelspec) for full " + dataset_name + ".")
print("Unit: " + unit_str + ".")
print("")
print("h5py version: {:s}".format(h5py.__version__))
print("librosa version: {:s}".format(librosa.__version__))
print("pandas version: {:s}".format(pd.__version__))
print("soundfile version: {:s}".format(sf.__version__))
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


# Start HDF5 group for log-mel-spectrograms (logmelspec).
lms_group = out_file.create_group("logmelspec")


# Open full audio file as FLAC.
recordings_name = "_".join([dataset_name, "full-audio"])
recordings_dir = os.path.join(data_dir, recordings_name)
recording_name = unit_str + ".flac"
recording_path = os.path.join(recordings_dir, recording_name)
full_audio = sf.SoundFile(recording_path)
full_audio_length = len(full_audio)


# Define a time sample for the middle of every audio clip.
sample_rate = localmodule.get_sample_rate()
lms_sample_rate = logmelspec_settings["sr"]
lms_hop_length = logmelspec_settings["hop_length"]
sample_float_step = 64 * lms_hop_length * sample_rate / lms_sample_rate
clip_length = int(np.round(0.5 * sample_rate))
half_clip_length = int(np.round(0.25 * sample_rate))
sample_start = half_clip_length
sample_stop = full_audio_length - half_clip_length
sample_range = np.arange(sample_start, sample_stop, sample_float_step)
sample_range = np.round(sample_range).astype('int')
n_clips = len(sample_range)
n_chunks = int(np.ceil(n_clips / n_clips_per_chunk))
samples_per_hop = lms_hop_length * sample_rate / lms_sample_rate


# Loop over chunks.
for chunk_id in range(n_chunks):
    # Load audio chunk.
    first_clip_id = chunk_id * n_clips_per_chunk
    last_clip_id = min((chunk_id+1) * n_clips_per_chunk, n_clips)
    chunk_range = range(first_clip_id, last_clip_id)
    chunk_sample_range = sample_range[chunk_range]
    chunk_start = chunk_sample_range[0] - half_clip_length
    chunk_stop = chunk_sample_range[-1] + half_clip_length
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
    logmelspec = 0.5 * librosa.logamplitude(melspec, ref=1.0)

    # Convert to single floating-point precision.
    chunk_logmelspec = logmelspec.astype('float32')

    # Loop over audio clips.
    for clip_id in range(n_clips_per_chunk):
        # Extract logmelspec clip in chunk
        mid_sample = chunk_sample_range[clip_id]
        mid_rel_sample = mid_sample - chunk_start
        mid_hop = int(np.round(mid_rel_sample / samples_per_hop))
        start_hop = mid_hop - int(np.round(half_clip_length / samples_per_hop))
        stop_hop = mid_hop + int(np.round(half_clip_length / samples_per_hop))
        clip_range = range(start_hop, stop_hop)
        clip_logmelspec = chunk_logmelspec[:, clip_range]

        # Define clip name.
        clip_name = str(mid_sample).zfill(9)

        # Store clip in HDF5 group.
        lms_group[clip_name] = clip_logmelspec


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
