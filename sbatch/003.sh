# This shell script executes the Slurm job for saving the BirdVox-70k data
# into HDF5 containers. Each HDF5 container corresponds to a different
# unit-augmentation pair, and contains audio, JAMS metadata, as well as
# metadata on the UTC starting time of the full night recording and
# the approximate GPS coordinates of the recording unit.

sbatch 003.sbatch
