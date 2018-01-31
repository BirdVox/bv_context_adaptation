import os
import sys

sys.path.append("../src")
import localmodule


# Define constants.
units = localmodule.get_units()
script_name = "053_evaluate-spectral-flux.py"


# Create folder.
script_dir = script_name[:-3]
os.makedirs(script_dir, exist_ok=True)
sbatch_dir = os.path.join(script_dir, "sbatch")
os.makedirs(sbatch_dir, exist_ok=True)
slurm_dir = os.path.join(script_dir, "slurm")
os.makedirs(slurm_dir, exist_ok=True)
file_path = os.path.join(sbatch_dir, script_name[:3] + ".sh")


# Open shell file.
with open(file_path, "w") as f:
    # Print header.
    f.write(
        "# This shell script executes the Slurm jobs for computing " +
        "spectral flux on continuous audio.\n")
    f.write("\n")

    # Loop over recording units.
    for unit_str in units:
        # Define job name.
        job_name = "_".join([script_name[:3], unit_str])
        sbatch_str = "sbatch " + job_name + ".sbatch"

        # Write SBATCH command to shell file.
        f.write(sbatch_str + "\n")
    f.write("\n")


# Grant permission to execute the shell file.
# https://stackoverflow.com/a/30463972
mode = os.stat(file_path).st_mode
mode |= (mode & 0o444) >> 2
os.chmod(file_path, mode)
