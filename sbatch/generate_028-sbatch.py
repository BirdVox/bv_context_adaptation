import os
import sys

sys.path.append("../src")
import localmodule


# Define constants.
script_name = "028_train-median-background-convnet.py"
script_path = os.path.join("..", "..", "..", "src", script_name)
units = localmodule.get_units()
bg_durations = [1, 2, 5, 10, 30, 60, 120, 300, 600, 1800, 3600, 7200]


# Create folders.
sbatch_dir = os.path.join(script_name[:-3], "sbatch")
os.makedirs(sbatch_dir, exist_ok=True)
slurm_dir = os.path.join(script_name[:-3], "slurm")
os.makedirs(slurm_dir, exist_ok=True)


# Loop over recording units.
for unit_str in units:

    # Loop over trials.
    for bg_duration in bg_durations:

        # Define string for background duration (prepend zeros).
        T_str = str(bg_duration).zfill(4)

        # Define file path.
        job_name = "_".join([script_name[:3], "T-" + T_str, unit_str])
        file_name = job_name + ".sbatch"
        file_path = os.path.join(sbatch_dir, file_name)

        # Define script.
        script_list = [script_path, T_str, unit_str]
        script_path_with_args = " ".join(script_list)

        # Open file.
        with open(file_path, "w") as f:
            f.write("#!/bin/bash\n")
            f.write("\n")
            f.write("#BATCH --job-name=" + job_name + "\n")
            f.write("#SBATCH --nodes=1\n")
            f.write("#SBATCH --tasks-per-node=1\n")
            f.write("#SBATCH --cpus-per-task=1\n")
            f.write("#SBATCH --time=08:00:00\n")
            f.write("#SBATCH --mem=8GB\n")
            f.write("#SBATCH --output=../slurm/slurm_" + job_name + "_%j.out\n")
            f.write("\n")
            f.write("module purge\n")
            f.write("\n")
            f.write("# The first argument is the name of the recording unit.\n")
            f.write("# The second argument is the duration of background.\n")
            f.write("python " + script_path_with_args)
