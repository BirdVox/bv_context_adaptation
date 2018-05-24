import datetime
import h5py
import librosa
import numpy as np
import os
import sys
import time

import localmodule


# Define constants.
data_dir = localmodule.get_data_dir()
dataset_name = localmodule.get_dataset_name()
sample_rate = localmodule.get_sample_rate()
args = sys.argv[1:]
aug_str = args[0]
instance_id = int(args[1])
instance_str = str(instance_id)
unit_str = args[2]
if aug_str == "original":
    instanced_aug_str = aug_str
else:
    instanced_aug_str = "-".join([aug_str, instance_str])
pcen_settings = localmodule.get_pcen_settings()


# Print header.
start_time = int(time.time())
print(str(datetime.datetime.now()) + " Start.")
print("Computing per-channel energy normalization (PCEN) for " +\
    dataset_name + " clips, with domain-specific librosa parameters.")
print("Unit: " + unit_str + ".")
print("Augmentation: " + instanced_aug_str + ".")
print("")
print("h5py version: {:s}".format(h5py.__version__))
print("librosa version: {:s}".format(librosa.__version__))
print("")


# Open HDF5 container of waveforms.
hdf5_dataset_name = "_".join([dataset_name, "hdf5"])
hdf5_dir = os.path.join(data_dir, hdf5_dataset_name)
in_aug_dir = os.path.join(hdf5_dir, aug_str)
hdf5_name = "_".join([dataset_name, instanced_aug_str, unit_str])
in_path = os.path.join(in_aug_dir, hdf5_name + ".hdf5")
in_file = h5py.File(in_path, "r")
sample_rate = in_file["sample_rate"].value


# Create HDF5 container of PCENs.
pcen_name = "_".join([dataset_name, "clip-birdpcen"])
pcen_dir = os.path.join(data_dir, pcen_name)
os.makedirs(pcen_dir, exist_ok=True)
out_aug_dir = os.path.join(pcen_dir, aug_str)
os.makedirs(out_aug_dir, exist_ok=True)
out_path = os.path.join(out_aug_dir, hdf5_name + ".hdf5")
try:
    os.remove(out_path)
except FileNotFoundError:
    pass
out_file = h5py.File(out_path)


# Copy over metadataself.
out_file["dataset_name"] = localmodule.get_dataset_name()
out_file["unit"] = unit_str
out_file["augmentation"] = aug_str
out_file["instance"] = instance_id
out_file["utc_start_time"] = in_file["utc_start_time"].value
gps_group = out_file.create_group("gps_coordinates")
gps_group["latitude"] = in_file["gps_coordinates"]["latitude"].value
gps_group["longitude"] = in_file["gps_coordinates"]["longitude"].value
settings_group = out_file.create_group("pcen_settings")
settings_group["fmax"] = pcen_settings["fmax"]
settings_group["fmin"] = pcen_settings["fmin"]
settings_group["hop_length"] = pcen_settings["hop_length"]
settings_group["n_fft"] = pcen_settings["n_fft"]
settings_group["n_mels"] = pcen_settings["n_mels"]
settings_group["sr"] = pcen_settings["sr"]
settings_group["win_length"] = pcen_settings["win_length"]
settings_group["window"] = pcen_settings["window"]


# These domain-specific parameters have shown to Gaussianize PCEN magnitudes.
settings_group["bias"] = 2.0
settings_group["time_constant"] = 0.015
settings_group["gain"] = 0.95
settings_group["power"] = 0.5
settings_group["eps"] = 1e-6


# List clips.
lms_group = out_file.create_group("pcen")
clip_names = list(in_file["waveforms"].keys())


# Loop over clips.
for clip_name in clip_names:

    # Load waveform.
    waveform = in_file["waveforms"][clip_name].value

    # Resample to 22050 Hz.
    waveform = librosa.resample(
        waveform, sample_rate, pcen_settings["sr"])

    # Compute Short-Term Fourier Transform (STFT).
    stft = librosa.stft(
        waveform,
        n_fft=pcen_settings["n_fft"],
        win_length=pcen_settings["win_length"],
        hop_length=pcen_settings["hop_length"],
        window=pcen_settings["window"])

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

    # PCEN with librosa.
    pcen = librosa.core.pcen(
        melspec,
        sr=settings_group["sr"].value,
        hop_length=settings_group["hop_length"].value,
        gain=settings_group["gain"].value,
        bias=settings_group["bias"].value,
        power=settings_group["power"].value,
        time_constant=settings_group["time_constant"].value,
        eps=settings_group["eps"].value)

    # Convert to single floating-point precision (32 bits).
    pcen = pcen.astype('float32')

    # Save.
    lms_group[clip_name] = pcen



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
