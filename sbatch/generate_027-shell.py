import os
import sys

sys.path.append("../src")
import localmodule


# Define constants.
units = localmodule.get_units()
bg_durations = [1, 2, 5, 10, 30, 60, 120, 300, 600, 1800, 3600, 7200]
script_name = "027_compute-clip-background-summaries.py"


# Create folder.
sbatch_dir = os.path.join(script_name[:-3], "sbatch")
os.makedirs(sbatch_dir, exist_ok=True)
slurm_dir = os.path.join(script_name[:-3], "slurm")
os.makedirs(slurm_dir, exist_ok=True)


# Loop over background durations.
for bg_duration in bg_durations:
    # Define string for background duration (prepend zeros).
    T_str = str(bg_duration).zfill(4)

    # Define file path.
    file_path = os.path.join(
        sbatch_dir, script_name[:3] + "_T-" + T_str + ".sh")

    # Open shell file.
    with open(file_path, "w") as f:
        # Print header.
        f.write(
            "# This shell script executes the Slurm jobs for computing " +
            "backgrounds on clips.\n")
        f.write("\n")

        # Loop over recording units.
        for unit_str in units:

            # Define job name.
            job_name = "_".join([script_name[:3], "T-" + T_str, unit_str])
            sbatch_str = "sbatch " + job_name + ".sbatch"

            # Write SBATCH command to shell file.
            f.write(sbatch_str + "\n")


    # Grant permission to execute the shell file.
    # https://stackoverflow.com/a/30463972
    mode = os.stat(file_path).st_mode
    mode |= (mode & 0o444) >> 2
    os.chmod(file_path, mode)
